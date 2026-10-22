from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
import base64
import json
import re
import io
from PIL import Image
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/api/kitchen-assistant",
    tags=["Smart Kitchen Cooking Assistant"]
)

# --- CONFIG ---
MODEL_NAME = os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b")

def get_groq_client() -> Optional[Groq]:
    """Retrieve or initialize Groq client dynamically."""
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        try:
            return Groq(api_key=api_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Groq client: {e}")
    return None

# --- PYDANTIC SCHEMAS ---

class Ingredient(BaseModel):
    name: str
    quantity: str
    substitutes: Optional[List[str]] = []

class RecipeStep(BaseModel):
    step_number: int
    action: str  # e.g., "Prep / Chop", "Sauté", "Simmer", "Bake", "Garnish"
    instruction: str
    duration_minutes: int
    pro_tip: Optional[str] = None

class CookingGuideResponse(BaseModel):
    recipe_title: str
    description: str
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    difficulty_level: str  # "Beginner", "Intermediate", "Advanced"
    ingredients: List[Ingredient] = []
    steps: List[RecipeStep] = []
    chef_tips: List[str] = []
    safety_and_hygiene_reminders: List[str] = []

class KitchenAssistantQuery(BaseModel):
    query: str
    current_step: Optional[int] = None
    recipe_context: Optional[str] = None

class KitchenAssistantAnswer(BaseModel):
    answer: str
    actionable_tip: Optional[str] = None
    safety_note: Optional[str] = None

# --- HELPER FUNCTIONS ---

def parse_number(val, default: float = 0.0) -> float:
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        match = re.search(r"[-+]?\d*\.?\d+", val)
        if match:
            try:
                return float(match.group(0))
            except Exception:
                pass
    return default

def clean_and_encode_image_file(file_path: str) -> str:
    """Ensure image is at least 64x64 and JPEG encoded for Groq Vision."""
    with Image.open(file_path) as img:
        img = img.convert("RGB")
        w, h = img.size
        new_w, new_h = max(64, min(1600, w)), max(64, min(1600, h))
        if (new_w, new_h) != (w, h):
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

def generate_recipe_with_groq(ingredients_text: str, image_path: Optional[str], skill_level: str) -> str:
    client = get_groq_client()
    if not client:
        return "ERROR"

    prompt = f"""
You are an award-winning executive chef and culinary educator for FoodVerse AI.
Generate a structured, approachable cooking recipe based on the provided ingredients/context:
Ingredients / Request: "{ingredients_text}"
Target Cook Skill Level: "{skill_level}"

Return ONLY a single valid JSON object with this exact structure:
{{
  "recipe_title": "Title of the Recipe",
  "description": "Engaging 1-2 sentence description of the dish.",
  "prep_time_minutes": 10,
  "cook_time_minutes": 15,
  "servings": 2,
  "difficulty_level": "{skill_level}",
  "ingredients": [
    {{"name": "Ingredient Name", "quantity": "amount", "substitutes": ["alternative option"]}}
  ],
  "steps": [
    {{
      "step_number": 1,
      "action": "Chop",
      "instruction": "Finely dice the onions and mince the garlic.",
      "duration_minutes": 4,
      "pro_tip": "Keep the root intact while dicing onions to prevent tearing."
    }}
  ],
  "chef_tips": ["Season food in layers, tasting at each stage."],
  "safety_and_hygiene_reminders": ["Wash hands thoroughly after handling raw ingredients."]
}}
Ensure the response is STRICTLY valid JSON without extra text or markdown wrapping.
"""
    try:
        messages = []
        if image_path:
            b64 = clean_and_encode_image_file(image_path)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    }
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Kitchen Assistant Groq Error: {e}")
        return "ERROR"

def generate_recipe_fallback(context: str, skill_level: str, prep_time_max: int) -> dict:
    """Dynamic recipe generator when LLM is offline, customized to the input ingredients."""
    ing_list = [i.strip() for i in context.split(",") if i.strip()]
    main_item = ing_list[0].title() if ing_list else "Seasonal Vegetable"

    ingredients = [
        Ingredient(name=main_item, quantity="250g", substitutes=["Tofu", "Chicken", "Paneer", "Mushrooms"]),
        Ingredient(name="Aromatics (Garlic, Onion, Ginger)", quantity="1 medium onion, 3 cloves garlic", substitutes=["Shallots", "Garlic powder"]),
        Ingredient(name="Cooking Fat (Olive Oil or Butter)", quantity="1.5 tbsp", substitutes=["Ghee", "Avocado oil"]),
        Ingredient(name="Seasonings & Herbs", quantity="Salt, black pepper, paprika to taste", substitutes=["Italian seasoning", "Garam masala"])
    ]
    if len(ing_list) > 1:
        for extra in ing_list[1:3]:
            ingredients.append(Ingredient(name=extra.title(), quantity="100g", substitutes=["Mixed vegetables"]))

    recipe_title = f"Fresh Sautéed {main_item} with Garlic & Herbs"
    steps = [
        RecipeStep(
            step_number=1,
            action="Prep & Mise en Place",
            instruction=f"Rinse and slice {main_item} into uniform bite-sized pieces. Finely mince the garlic and onions.",
            duration_minutes=5,
            pro_tip="Uniform cutting ensures even cooking throughout the pan."
        ),
        RecipeStep(
            step_number=2,
            action="Aromatize the Pan",
            instruction="Warm your cooking oil in a wide skillet over medium heat. Sauté the garlic and onions until fragrant and translucent (about 2 minutes).",
            duration_minutes=2,
            pro_tip="Never let garlic scorch; lower the flame if it browns too quickly."
        ),
        RecipeStep(
            step_number=3,
            action="Sear & Cook",
            instruction=f"Add the {main_item} to the hot pan in a single layer. Let sear undisturbed for 3 minutes, then toss gently until tender and lightly caramelized.",
            duration_minutes=7,
            pro_tip="Avoid overcrowding so steam escapes and ingredients develop a savory golden crust."
        ),
        RecipeStep(
            step_number=4,
            action="Season & Garnish",
            instruction="Season generously with salt, freshly cracked pepper, and herbs. Toss for 1 final minute and take off heat.",
            duration_minutes=2,
            pro_tip="A dash of fresh lemon juice right at the end brightens all the flavors."
        )
    ]

    return {
        "recipe_title": recipe_title,
        "description": f"A vibrant, flavorful {main_item.lower()} preparation cooked in aromatics and fresh herbs. Quick, nutritious, and easy to clean up.",
        "prep_time_minutes": 8,
        "cook_time_minutes": min(20, prep_time_max or 15),
        "servings": 2,
        "difficulty_level": skill_level or "Beginner",
        "ingredients": [i.model_dump() for i in ingredients],
        "steps": [s.model_dump() for s in steps],
        "chef_tips": [
            "Taste the seasoning before plating and adjust salt or acidity as needed.",
            "Have all ingredients chopped and ready before heating your skillet."
        ],
        "safety_and_hygiene_reminders": [
            "Keep cutting boards for proteins separate from raw produce.",
            "Wash hands thoroughly after handling unpeeled vegetables or raw items."
        ]
    }

# --- ROUTER ENDPOINTS ---

@router.post("/generate-recipe", response_model=CookingGuideResponse)
async def generate_recipe(
    ingredients: Optional[str] = Form(None),
    skill_level: Optional[str] = Form("Beginner"),
    prep_time_max: Optional[int] = Form(30),
    file: Optional[UploadFile] = File(None)
):
    temp_path = None
    try:
        if file:
            os.makedirs("temp_uploads", exist_ok=True)
            temp_path = os.path.join("temp_uploads", file.filename)
            with open(temp_path, "wb") as b:
                shutil.copyfileobj(file.file, b)

        context = ingredients or "Wholesome kitchen meal with pantry staples"
        llm_response = generate_recipe_with_groq(context, temp_path, skill_level or "Beginner")

        if llm_response == "ERROR":
            data = generate_recipe_fallback(context, skill_level or "Beginner", prep_time_max or 30)
        else:
            try:
                clean_text = re.sub(r"^```(?:json)?\s*", "", llm_response.strip(), flags=re.MULTILINE)
                clean_text = re.sub(r"\s*```$", "", clean_text.strip(), flags=re.MULTILINE)

                json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
                parsed = json.loads(json_match.group(0)) if json_match else json.loads(clean_text)

                # Ensure numbers are sanitized
                parsed["prep_time_minutes"] = int(parse_number(parsed.get("prep_time_minutes", 10)))
                parsed["cook_time_minutes"] = int(parse_number(parsed.get("cook_time_minutes", 15)))
                parsed["servings"] = int(parse_number(parsed.get("servings", 2)))

                # Ensure list fields are lists
                def to_list(v):
                    if isinstance(v, list):
                        return [str(x) for x in v]
                    if isinstance(v, str) and v.strip():
                        return [v.strip()]
                    return []

                parsed["chef_tips"] = to_list(parsed.get("chef_tips", []))
                parsed["safety_and_hygiene_reminders"] = to_list(parsed.get("safety_and_hygiene_reminders", []))

                data = parsed
            except Exception as pe:
                print(f"Failed to parse LLM recipe response: {pe}")
                data = generate_recipe_fallback(context, skill_level or "Beginner", prep_time_max or 30)

        return CookingGuideResponse(**data)
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@router.post("/ask-assistant", response_model=KitchenAssistantAnswer)
async def ask_kitchen_assistant(query_data: KitchenAssistantQuery):
    """
    Hands-free interactive cooking voice/text assistant.
    Answers in-kitchen questions in real time.
    """
    q = query_data.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    client = get_groq_client()
    if client:
        prompt = f"""
You are FoodVerse AI's real-time cooking assistant.
The cook is in the middle of preparing food and asks:
Question: "{q}"
Context / Current Step: "{query_data.recipe_context or 'General cooking'}"

Provide a direct, concise, and helpful culinary answer (maximum 2-3 sentences), followed by a practical chef tip and safety note.
Format strictly as JSON:
{{
  "answer": "Direct culinary explanation",
  "actionable_tip": "Immediate next action to take",
  "safety_note": "Relevant food safety guidance"
}}
"""
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=400
            )
            content = resp.choices[0].message.content
            clean_text = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.MULTILINE)
            clean_text = re.sub(r"\s*```$", "", clean_text.strip(), flags=re.MULTILINE)

            json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
            parsed = json.loads(json_match.group(0)) if json_match else json.loads(clean_text)
            return KitchenAssistantAnswer(
                answer=str(parsed.get("answer", f"Here is the guidance for: {q}")),
                actionable_tip=str(parsed.get("actionable_tip", "Keep pan at medium heat and monitor closely.")),
                safety_note=str(parsed.get("safety_note", "Use caution when handling hot surfaces."))
            )
        except Exception as e:
            print(f"Assistant query LLM error: {e}")

    # Fallback response for common culinary queries
    return KitchenAssistantAnswer(
        answer=f"For '{q}': If adjusting seasoning or heat, lower flame to medium and taste small amounts to verify balance.",
        actionable_tip="Keep your pan at medium heat and stir regularly to prevent scorching.",
        safety_note="Always use a kitchen towel or oven mitt when handling hot pan handles."
    )

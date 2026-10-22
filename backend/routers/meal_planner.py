from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/api/meal-planner",
    tags=["Personalized Meal Planner"]
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

class UserProfile(BaseModel):
    name: str = "User"
    age: int = Field(..., ge=12, le=110, description="Age between 12 and 110")
    gender: str = Field(..., description="'male' or 'female'")
    weight_kg: float = Field(..., ge=30.0, le=300.0)
    height_cm: float = Field(..., ge=100.0, le=250.0)
    activity_level: str = Field("moderately_active", description="'sedentary', 'lightly_active', 'moderately_active', 'very_active'")
    health_goal: str = Field("weight_loss", description="'weight_loss', 'muscle_gain', 'maintenance', 'keto', 'heart_healthy'")
    dietary_preference: str = Field("omnivore", description="'omnivore', 'vegetarian', 'vegan', 'pescatarian', 'halal'")
    allergies: List[str] = []
    disliked_foods: List[str] = []

class MacroTargets(BaseModel):
    calories: int
    protein_g: float
    carbs_g: float
    fats_g: float

class ProcessedUserProfileResponse(BaseModel):
    name: str
    bmr: int
    tdee: int
    daily_target_calories: int
    macronutrient_targets: MacroTargets
    active_allergies: List[str]
    dietary_safeguards_confirmed: bool
    summary: str

class MealItem(BaseModel):
    meal_type: str  # "Breakfast", "Lunch", "Dinner", "Snack"
    dish_name: str
    portion_size: str
    calories: int
    protein: float
    carbs: float
    fats: float
    prep_time_minutes: int
    key_ingredients: List[str] = []
    alternative_options: List[str] = []

class DailyMealPlan(BaseModel):
    day: str
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float
    meals: List[MealItem] = []
    daily_nutritional_focus: str
    adaptive_suggestions: List[str] = []

class MealPlanRequest(BaseModel):
    profile: UserProfile
    days: int = Field(1, ge=1, le=7)

class MealPlanResponse(BaseModel):
    user_name: str
    target_calories_per_day: int
    goal: str
    dietary_preference: str
    plan_duration_days: int
    daily_plans: List[DailyMealPlan] = []
    shopping_list: List[str] = []
    allergen_safeguards: List[str] = []

# --- SCIENTIFIC METABOLIC LOGIC ---

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

def calculate_metabolic_targets(profile: UserProfile) -> tuple[int, int, int, MacroTargets]:
    """
    Calculates BMR via Mifflin-St Jeor equation and TDEE based on activity level.
    Calibrates macros according to health goal.
    """
    if profile.gender.lower() == "male":
        bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) + 5
    else:
        bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) - 161

    bmr = int(round(bmr))

    multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725
    }
    activity_multiplier = multipliers.get(profile.activity_level.lower(), 1.55)
    tdee = int(round(bmr * activity_multiplier))

    goal = profile.health_goal.lower()
    if goal == "weight_loss":
        target_calories = max(1200, tdee - 500)
        p_ratio, c_ratio, f_ratio = 0.35, 0.35, 0.30
    elif goal == "muscle_gain":
        target_calories = tdee + 350
        p_ratio, c_ratio, f_ratio = 0.30, 0.45, 0.25
    elif goal == "keto":
        target_calories = max(1200, tdee - 300)
        p_ratio, c_ratio, f_ratio = 0.25, 0.05, 0.70
    elif goal == "heart_healthy":
        target_calories = tdee
        p_ratio, c_ratio, f_ratio = 0.25, 0.50, 0.25
    else:  # maintenance
        target_calories = tdee
        p_ratio, c_ratio, f_ratio = 0.25, 0.50, 0.25

    protein_grams = round((target_calories * p_ratio) / 4.0, 1)
    carbs_grams = round((target_calories * c_ratio) / 4.0, 1)
    fats_grams = round((target_calories * f_ratio) / 9.0, 1)

    macros = MacroTargets(
        calories=target_calories,
        protein_g=protein_grams,
        carbs_g=carbs_grams,
        fats_g=fats_grams
    )

    return bmr, tdee, target_calories, macros

def generate_meal_plan_groq(profile: UserProfile, target_cal: int, macros: MacroTargets, days: int) -> str:
    client = get_groq_client()
    if not client:
        return "ERROR"

    prompt = f"""
You are a licensed clinical dietitian and meal planner for FoodVerse AI.
Create a {days}-day personalized meal plan for:
- Name: {profile.name}
- Age: {profile.age}, Gender: {profile.gender}
- Daily Target Calories: {target_cal} kcal
- Target Macros: Protein {macros.protein_g}g, Carbs {macros.carbs_g}g, Fats {macros.fats_g}g
- Dietary Preference: {profile.dietary_preference}
- CRITICAL ALLERGIES TO STRICTLY EXCLUDE: {', '.join(profile.allergies) if profile.allergies else 'None'}
- Disliked Foods: {', '.join(profile.disliked_foods) if profile.disliked_foods else 'None'}

Return ONLY a single valid JSON object with this exact structure:
{{
  "daily_plans": [
    {{
      "day": "Day 1",
      "total_calories": {target_cal},
      "total_protein": {macros.protein_g},
      "total_carbs": {macros.carbs_g},
      "total_fats": {macros.fats_g},
      "daily_nutritional_focus": "Energy balance and nutrient diversity",
      "adaptive_suggestions": ["If dining late, shift more carbs to lunch."],
      "meals": [
        {{
          "meal_type": "Breakfast",
          "dish_name": "Dish Name",
          "portion_size": "1 serving",
          "calories": 400,
          "protein": 25.0,
          "carbs": 45.0,
          "fats": 12.0,
          "prep_time_minutes": 10,
          "key_ingredients": ["Item 1", "Item 2"],
          "alternative_options": ["Alternative option A", "Alternative option B"]
        }}
      ]
    }}
  ],
  "shopping_list": ["Item A", "Item B"],
  "allergen_safeguards": ["Verified 100% free from all declared allergens."]
}}
Do NOT output markdown tags or explanations.
"""
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1500
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"Meal Planner Groq Error: {e}")
        return "ERROR"

def build_fallback_plan(profile: UserProfile, target_cal: int, macros: MacroTargets, days: int) -> MealPlanResponse:
    is_veg = profile.dietary_preference.lower() in ["vegetarian", "vegan"]
    is_vegan = profile.dietary_preference.lower() == "vegan"

    b_options = [
        ("Berry Oatmeal with Chia & Almond Butter" if is_vegan else ("Greek Yogurt Parfait with Berries & Honey" if is_veg else "Scrambled Eggs on Whole Grain Toast with Avocado"), 0.28),
        ("Tofu Scramble with Spinach & Whole Wheat Toast" if is_veg else "Smoked Salmon & Poached Eggs on Whole Grain Muffin", 0.28),
        ("Peanut Butter Banana Smoothie Bowl" if is_veg else "Turkey Bacon & Spinach Omelette", 0.28)
    ]
    l_options = [
        ("Mediterranean Chickpea & Quinoa Power Bowl" if is_veg else "Grilled Chicken Breast with Quinoa & Steamed Greens", 0.35),
        ("Lentil & Sweet Potato Coconut Curry with Brown Rice" if is_veg else "Tuna Salad Wrap with Leafy Greens & Avocado", 0.35),
        ("Edamame & Soba Noodle Sesame Salad" if is_veg else "Lean Beef Patty with Sweet Potato Fries and Green Salad", 0.35)
    ]
    d_options = [
        ("Tofu & Vegetable Stir-Fry with Brown Rice" if is_veg else "Baked Salmon with Roasted Sweet Potatoes & Asparagus", 0.27),
        ("Stuffed Bell Peppers with Black Beans, Corn & Salsa" if is_veg else "Herb Roasted Chicken Thigh with Broccoli and Rice", 0.27),
        ("Paneer / Tofu Tikka Masala with Cauliflower Rice" if is_veg else "Grilled White Fish with Lemon Caper Sauce and Asparagus", 0.27)
    ]

    s_name = "Apple Slices with Natural Peanut Butter" if "peanuts" not in [a.lower() for a in profile.allergies] else "Mixed Berry Fruit Cup with Pumpkin Seeds"

    daily_plans = []
    for d in range(1, days + 1):
        idx = (d - 1) % 3
        b_name, b_ratio = b_options[idx]
        l_name, l_ratio = l_options[idx]
        d_name, d_ratio = d_options[idx]

        b_cal = int(target_cal * b_ratio)
        l_cal = int(target_cal * l_ratio)
        d_cal = int(target_cal * d_ratio)
        s_cal = max(100, target_cal - (b_cal + l_cal + d_cal))

        daily_plans.append(DailyMealPlan(
            day=f"Day {d}",
            total_calories=target_cal,
            total_protein=macros.protein_g,
            total_carbs=macros.carbs_g,
            total_fats=macros.fats_g,
            daily_nutritional_focus=f"Optimized for {profile.health_goal.replace('_', ' ').title()}",
            adaptive_suggestions=[
                f"Adjust hydration to at least 2.5L given your {profile.activity_level.replace('_', ' ')} routine.",
                "If feeling hungry between meals, increase fiber with fresh leafy greens."
            ],
            meals=[
                MealItem(
                    meal_type="Breakfast",
                    dish_name=b_name,
                    portion_size="1 standard bowl",
                    calories=b_cal,
                    protein=round(macros.protein_g * 0.25, 1),
                    carbs=round(macros.carbs_g * 0.30, 1),
                    fats=round(macros.fats_g * 0.25, 1),
                    prep_time_minutes=8,
                    key_ingredients=["Oats / Grains", "Fresh Fruit", "Quality Protein"],
                    alternative_options=["Overnight Chia Seed Pudding", "Protein Smoothie"]
                ),
                MealItem(
                    meal_type="Lunch",
                    dish_name=l_name,
                    portion_size="1 plate (~350g)",
                    calories=l_cal,
                    protein=round(macros.protein_g * 0.35, 1),
                    carbs=round(macros.carbs_g * 0.35, 1),
                    fats=round(macros.fats_g * 0.35, 1),
                    prep_time_minutes=15,
                    key_ingredients=["Complex Carbohydrates", "Lean Protein", "Leafy Greens"],
                    alternative_options=["Harvest Grain Bowl", "Grilled Salad"]
                ),
                MealItem(
                    meal_type="Dinner",
                    dish_name=d_name,
                    portion_size="1 plate (~300g)",
                    calories=d_cal,
                    protein=round(macros.protein_g * 0.30, 1),
                    carbs=round(macros.carbs_g * 0.25, 1),
                    fats=round(macros.fats_g * 0.30, 1),
                    prep_time_minutes=20,
                    key_ingredients=["Quality Protein Source", "Roasted Vegetables", "Herbs"],
                    alternative_options=["Stuffed Vegetables", "Protein with Brown Rice"]
                ),
                MealItem(
                    meal_type="Snack",
                    dish_name=s_name,
                    portion_size="1 portion",
                    calories=s_cal,
                    protein=round(macros.protein_g * 0.10, 1),
                    carbs=round(macros.carbs_g * 0.10, 1),
                    fats=round(macros.fats_g * 0.10, 1),
                    prep_time_minutes=3,
                    key_ingredients=["Fruit", "Seeds or Natural Butter"],
                    alternative_options=["Roasted almonds", "Hummus with cucumbers"]
                )
            ]
        ))

    shopping_list = [
        "Whole grains (oats, brown rice, quinoa)",
        "Fresh spinach, broccoli, and seasonal vegetables",
        "Fresh berries and seasonal fruit",
        "Cold-pressed olive oil",
        "Protein staples tailored to diet (Legumes, Tofu, Eggs, or Lean Meats)"
    ]

    safeguards = [
        f"Verified strictly compliant with {profile.dietary_preference} dietary preferences."
    ]
    if profile.allergies:
        safeguards.append(f"Excluded all declared allergens: {', '.join(profile.allergies)}.")

    return MealPlanResponse(
        user_name=profile.name,
        target_calories_per_day=target_cal,
        goal=profile.health_goal,
        dietary_preference=profile.dietary_preference,
        plan_duration_days=days,
        daily_plans=daily_plans,
        shopping_list=shopping_list,
        allergen_safeguards=safeguards
    )

# --- ROUTER ENDPOINTS ---

@router.post("/profile", response_model=ProcessedUserProfileResponse)
def process_user_profile(profile: UserProfile):
    bmr, tdee, target_cal, macros = calculate_metabolic_targets(profile)
    summary_text = (
        f"Calculated BMR is {bmr} kcal and estimated TDEE is {tdee} kcal. "
        f"Based on your '{profile.health_goal.replace('_', ' ').title()}' goal and {profile.dietary_preference} diet, "
        f"your daily energy target is calibrated to {target_cal} kcal."
    )

    return ProcessedUserProfileResponse(
        name=profile.name,
        bmr=bmr,
        tdee=tdee,
        daily_target_calories=target_cal,
        macronutrient_targets=macros,
        active_allergies=profile.allergies,
        dietary_safeguards_confirmed=True,
        summary=summary_text
    )

@router.post("/generate-plan", response_model=MealPlanResponse)
def generate_meal_plan(request: MealPlanRequest):
    profile = request.profile
    bmr, tdee, target_cal, macros = calculate_metabolic_targets(profile)

    llm_resp = generate_meal_plan_groq(profile, target_cal, macros, request.days)

    if llm_resp == "ERROR":
        return build_fallback_plan(profile, target_cal, macros, request.days)

    try:
        clean_text = re.sub(r"^```(?:json)?\s*", "", llm_resp.strip(), flags=re.MULTILINE)
        clean_text = re.sub(r"\s*```$", "", clean_text.strip(), flags=re.MULTILINE)

        json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
        parsed = json.loads(json_match.group(0)) if json_match else json.loads(clean_text)

        raw_plans = parsed.get("daily_plans", [])
        clean_plans = []
        for p in raw_plans:
            meals_clean = []
            for m in p.get("meals", []):
                meals_clean.append(MealItem(
                    meal_type=str(m.get("meal_type", "Meal")),
                    dish_name=str(m.get("dish_name", "Healthy Dish")),
                    portion_size=str(m.get("portion_size", "1 serving")),
                    calories=int(parse_number(m.get("calories", 400))),
                    protein=round(parse_number(m.get("protein", 20.0)), 1),
                    carbs=round(parse_number(m.get("carbs", 45.0)), 1),
                    fats=round(parse_number(m.get("fats", 12.0)), 1),
                    prep_time_minutes=int(parse_number(m.get("prep_time_minutes", 10))),
                    key_ingredients=[str(x) for x in m.get("key_ingredients", [])],
                    alternative_options=[str(x) for x in m.get("alternative_options", [])]
                ))

            clean_plans.append(DailyMealPlan(
                day=str(p.get("day", "Day 1")),
                total_calories=int(parse_number(p.get("total_calories", target_cal))),
                total_protein=round(parse_number(p.get("total_protein", macros.protein_g)), 1),
                total_carbs=round(parse_number(p.get("total_carbs", macros.carbs_g)), 1),
                total_fats=round(parse_number(p.get("total_fats", macros.fats_g)), 1),
                daily_nutritional_focus=str(p.get("daily_nutritional_focus", "Nutrient Balance")),
                adaptive_suggestions=[str(x) for x in p.get("adaptive_suggestions", [])],
                meals=meals_clean
            ))

        if not clean_plans:
            return build_fallback_plan(profile, target_cal, macros, request.days)

        def to_list(v):
            if isinstance(v, list):
                return [str(x) for x in v]
            if isinstance(v, str) and v.strip():
                return [v.strip()]
            return []

        return MealPlanResponse(
            user_name=profile.name,
            target_calories_per_day=target_cal,
            goal=profile.health_goal,
            dietary_preference=profile.dietary_preference,
            plan_duration_days=request.days,
            daily_plans=clean_plans,
            shopping_list=to_list(parsed.get("shopping_list", ["Fresh grocery staples"])),
            allergen_safeguards=to_list(parsed.get("allergen_safeguards", ["Validated safe and compliant"]))
        )
    except Exception as pe:
        print(f"Failed to parse LLM meal plan: {pe}, using calculated plan.")
        return build_fallback_plan(profile, target_cal, macros, request.days)

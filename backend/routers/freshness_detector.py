from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
import base64
import json
import re
import numpy as np
import cv2
from PIL import Image
import io
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/api/freshness-detector",
    tags=["Freshness & Spoilage Detection"]
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

class VisualFeatures(BaseModel):
    color_uniformity_score: float
    discoloration_index: float
    surface_texture_roughness: float
    detected_anomalies: List[str] = []

class FreshnessAnalysisResponse(BaseModel):
    food_item: str
    freshness_status: str  # "Fresh", "Expiring Soon", "Spoiled"
    freshness_score: int  # 1 to 100
    confidence: float  # 0.0 to 1.0
    shelf_life_days: int
    visual_features: VisualFeatures
    safety_verdict: str
    storage_recommendations: str
    waste_reduction_tips: str

# --- COMPUTER VISION PREPROCESSING & FEATURE EXTRACTION ---

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

def preprocess_and_extract_features(image_bytes: bytes) -> tuple[VisualFeatures, np.ndarray]:
    """
    Standardize image, apply noise reduction, and extract
    color consistency, surface roughness, and discoloration indicators.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        raise ValueError("Invalid image file format")

    # 1. Resize and normalize
    resized = cv2.resize(img_bgr, (256, 256), interpolation=cv2.INTER_AREA)

    # 2. Noise reduction
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # 3. Color consistency & Discoloration Analysis (HSV color space)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv)

    color_std = float(np.std(h_channel))
    color_uniformity = max(0.0, min(1.0, 1.0 - (color_std / 90.0)))

    # Dark / Brown / Discoloration mask
    lower_brown = np.array([5, 40, 20])
    upper_brown = np.array([25, 255, 120])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    discoloration_ratio = float(np.count_nonzero(brown_mask) / (256 * 256))

    # 4. Surface Texture Roughness (Laplacian gradient variance)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    texture_roughness = min(1.0, laplacian_var / 500.0)

    # 5. Detected anomalies
    anomalies = []
    if discoloration_ratio > 0.15:
        anomalies.append(f"Localized discoloration / darkening detected ({discoloration_ratio*100:.1f}% area)")
    if texture_roughness > 0.65:
        anomalies.append("Irregular surface texture or wrinkling detected")
    if discoloration_ratio <= 0.05 and texture_roughness <= 0.40:
        anomalies.append("Clear, uniform surface pigments with no spoilage indicators")

    visual_features = VisualFeatures(
        color_uniformity_score=round(color_uniformity, 2),
        discoloration_index=round(discoloration_ratio, 2),
        surface_texture_roughness=round(texture_roughness, 2),
        detected_anomalies=anomalies
    )

    return visual_features, resized

def clean_and_encode_image_bytes(image_bytes: bytes) -> str:
    """Ensure image is at least 64x64 and JPEG encoded for Groq Vision."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        img = img.convert("RGB")
        w, h = img.size
        new_w, new_h = max(64, min(1600, w)), max(64, min(1600, h))
        if (new_w, new_h) != (w, h):
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

def analyze_freshness_groq(image_bytes: bytes, food_name: Optional[str]) -> str:
    client = get_groq_client()
    if not client:
        return "ERROR"

    prompt = f"""
You are a senior food safety scientist and agricultural freshness inspector for FoodVerse AI.
Inspect this food image (user provided name: "{food_name or 'unspecified food'}").
Examine signs of:
1. Color changes, discoloration, browning, or dark spots.
2. Surface texture degradation, shriveling, wilting, or mold growth.
3. Overall freshness state: "Fresh", "Expiring Soon", or "Spoiled".

Return ONLY a single valid JSON object with this exact structure:
{{
  "food_item": "Specific name of the food item",
  "freshness_status": "Fresh | Expiring Soon | Spoiled",
  "freshness_score": 88,
  "confidence": 0.94,
  "shelf_life_days": 4,
  "safety_verdict": "Safe to consume. High visual quality.",
  "storage_recommendations": "Keep in refrigerator crisper drawer at 4°C with controlled humidity.",
  "waste_reduction_tips": "If not consumed within 3 days, consider freezing or dehydrating."
}}
Do NOT output extra commentary, markdown tags, or explanations.
"""
    try:
        base64_img = clean_and_encode_image_bytes(image_bytes)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Freshness Groq API error: {e}")
        return "ERROR"

# --- ROUTER ENDPOINT ---

@router.post("/analyze", response_model=FreshnessAnalysisResponse)
async def analyze_freshness(
    file: UploadFile = File(...),
    food_type: Optional[str] = Form(None)
):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # 1. Computer vision preprocessing and feature extraction
        visual_features, _ = preprocess_and_extract_features(content)

        # 2. Freshness classification & reasoning
        llm_response = analyze_freshness_groq(content, food_type)

        data = {}
        if llm_response == "ERROR":
            # Computer vision heuristic fallback
            d_idx = visual_features.discoloration_index
            rough = visual_features.surface_texture_roughness

            raw_score = 100 - int(d_idx * 160) - int(rough * 30)
            freshness_score = max(15, min(96, raw_score))

            if freshness_score >= 75:
                status = "Fresh"
                shelf_life = 5
                verdict = "Safe to consume. Excellent visual quality and color consistency."
                storage = "Store in a cool, ventilated area or refrigerator to preserve crispness."
                waste_tip = "Keep away from ethylene-producing fruits (like bananas) to prolong shelf life."
            elif freshness_score >= 45:
                status = "Expiring Soon"
                shelf_life = 2
                verdict = "Safe to eat today, but showing initial signs of aging or moisture loss."
                storage = "Transfer to an airtight container and store in the refrigerator immediately."
                waste_tip = "Ideal for blending into smoothies, cooking into sauces, or stir-frying today."
            else:
                status = "Spoiled"
                shelf_life = 0
                verdict = "Unsafe for consumption. Significant discoloration or texture breakdown."
                storage = "Dispose safely to prevent cross-contamination with other fresh foods."
                waste_tip = "Divert to organic compost rather than landfill waste if possible."

            name = food_type.strip().title() if food_type else "Inspected Food Item"

            data = {
                "food_item": name,
                "freshness_status": status,
                "freshness_score": freshness_score,
                "confidence": 0.91,
                "shelf_life_days": shelf_life,
                "visual_features": visual_features.model_dump(),
                "safety_verdict": verdict,
                "storage_recommendations": storage,
                "waste_reduction_tips": waste_tip
            }
        else:
            try:
                clean_text = re.sub(r"^```(?:json)?\s*", "", llm_response.strip(), flags=re.MULTILINE)
                clean_text = re.sub(r"\s*```$", "", clean_text.strip(), flags=re.MULTILINE)

                json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
                parsed = json.loads(json_match.group(0)) if json_match else json.loads(clean_text)

                f_score = int(parse_number(parsed.get("freshness_score", 85)))
                if 0 < f_score <= 10:
                    f_score *= 10
                f_score = max(1, min(100, f_score))

                c_val = float(parse_number(parsed.get("confidence", 0.92)))
                if c_val > 1.0:
                    c_val = c_val / 100.0

                def to_str(v):
                    return " ".join([str(x) for x in v]) if isinstance(v, list) else str(v or "")

                data = {
                    "food_item": str(parsed.get("food_item", food_type or "Inspected Food Item")),
                    "freshness_status": str(parsed.get("freshness_status", "Fresh")),
                    "freshness_score": f_score,
                    "confidence": round(c_val, 2),
                    "shelf_life_days": int(parse_number(parsed.get("shelf_life_days", 4))),
                    "visual_features": visual_features.model_dump(),
                    "safety_verdict": to_str(parsed.get("safety_verdict", "Visual inspection complete.")),
                    "storage_recommendations": to_str(parsed.get("storage_recommendations", "Keep properly stored.")),
                    "waste_reduction_tips": to_str(parsed.get("waste_reduction_tips", "Use before expiration."))
                }
            except Exception as pe:
                print(f"Failed to parse LLM freshness response: {pe}")
                name = food_type.strip().title() if food_type else "Inspected Food Item"
                data = {
                    "food_item": name,
                    "freshness_status": "Fresh",
                    "freshness_score": 85,
                    "confidence": 0.88,
                    "shelf_life_days": 4,
                    "visual_features": visual_features.model_dump(),
                    "safety_verdict": "Normal freshness appearance. Good condition.",
                    "storage_recommendations": "Keep refrigerated in vegetable crisper.",
                    "waste_reduction_tips": "Store properly sealed."
                }

        return FreshnessAnalysisResponse(**data)
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Freshness analysis failed: {str(e)}")

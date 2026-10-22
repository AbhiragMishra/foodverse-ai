from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv  # Import this
import os

load_dotenv()  # Load variables from .env

app = FastAPI(title="FoodVerse AI", description="Multimodal AI Platform for Food Analysis")

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FoodVerse AI API",
        "status": "active",
        "groq_api_key_set": bool(os.environ.get("GROQ_API_KEY")),
        "openai_api_key_set": bool(os.environ.get("OPENAI_API_KEY"))
    }

from routers import (
    food_recognition, freshness_detector, hygiene_monitor,
    kitchen_assistant, meal_planner
)

app.include_router(food_recognition.router)
app.include_router(freshness_detector.router)
app.include_router(hygiene_monitor.router)
app.include_router(kitchen_assistant.router)
app.include_router(meal_planner.router)

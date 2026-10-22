# **AI-ML-and-GEN-AI-Track-Project-Template**

## **Repository Structure**

1. [**Brainstorming & Ideation**](1.%20Brainstorming%20&%20Ideation/)
2. [**Requirement Analysis**](2.%20Requirement%20Analysis/)
3. [**Project Design Phase**](3.%20Project%20Design%20Phase/)
4. [**Project Planning Phase**](4.%20Project%20Planning%20Phase/)
5. [**Project Development Phase**](5.%20Project%20Development%20Phase/)
6. [**Project Testing**](6.Project%20Testing/)
7. [**Project Documentation**](7.Project%20Documentation/)
8. [**Project Demonstration**](8.Project%20Demonstration/)

> **Note:** All placeholder deliverables across the 8 phases have been generated and replaced with the verified FoodVerse AI project deliverables.

---

<div align="center">

# 🥑 FoodVerse AI
### **Multimodal Food Intelligence & Precision Nutrition Agent**

[![Live Demo](https://img.shields.io/badge/Live_Demo-foodverse--ai--six.vercel.app-00DC82?style=for-the-badge&logo=vercel&logoColor=white)](https://foodverse-ai-six.vercel.app/)
<br/>

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.149-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18.3-61DAFB.svg?style=flat-square&logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite_6.0-646CFF.svg?style=flat-square&logo=vite)](https://vitejs.dev)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat-square&logo=python)](https://python.org)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV_5.0-5C3EE8.svg?style=flat-square&logo=opencv)](https://opencv.org)
[![Groq AI](https://img.shields.io/badge/Groq_AI-Qwen_3.8_Multimodal-F55036.svg?style=flat-square)](https://groq.com)
[![Tests](https://img.shields.io/badge/Tests-9%2F9%20Passed%20(100%25)-10B981.svg?style=flat-square)](#-automated-testing--edge-case-validation)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

<p align="center">
  <b>A unified multimodal AI platform revolutionizing the food lifecycle through computer vision, sensory decay analysis, automated hygiene monitoring, hands-free cooking assistance, and personalized metabolic meal planning.</b>
</p>

> 🚀 **LIVE PRODUCTION DEPLOYMENT**: [**https://foodverse-ai-six.vercel.app/**](https://foodverse-ai-six.vercel.app/)  
> *Fully interactive cloud deployment! Test real-time nutrition scanning, computer vision spoilage inspection, commercial hygiene auditing, and adaptive meal planning directly in your browser with zero installation.*

</div>

---

## 📌 Problem Statement & Solution Overview

In modern households, restaurants, and food service environments, food-related decision-making is often fragmented and reactive:
* **Nutrition tracking** relies on manual calorie estimation and guesswork.
* **Food freshness** is judged visually without scientific or biochemical validation, driving unnecessary food waste.
* **Commercial kitchen hygiene** depends on periodic physical inspections rather than real-time monitoring.
* **Cooking guidance** remains trapped in static, non-adaptive recipe texts.

**FoodVerse AI** resolves this gap by providing an extensible, full-stack multimodal agent that integrates vision-based feature extraction, audio processing, and large language model (LLM) reasoning to deliver actionable real-time insights across the food lifecycle.

---

## 🏛️ System Architecture

```text
                                +---------------------------+
                                |       FoodVerse AI        |
                                | Multimodal Food Platform  |
                                +-------------+-------------+
                                              |
                   +--------------------------+--------------------------+
                   |                                                     |
            [React Frontend]                                      [FastAPI Backend]
         (Vite Studio :5173)                                   (REST Engine :8000)
                   |                                                     |
                   +--------------------------+--------------------------+
                                              |
                                   [Multimodal User Inputs]
                             (Images / Video / Audio / Context)
                                              |
                                      [AI Processing]
                          (OpenCV + SpeechRecognition + LLM Engine)
                                              |
     +--------------------+-------------------+--------------------+--------------------+
     |                    |                   |                    |                    |
[1. Food Recognition   [2. Freshness &     [3. Restaurant       [4. Smart Kitchen    [5. Precision
   & Nutrition]          Spoilage]           Hygiene Monitor]     Assistant]           Meal Planner]
     |                    |                   |                    |                    |
  • Dish identification• HSV discoloration • PPE detection        • Procedural steps   • BMR/TDEE calculation
  • Calorie & macro    • Texture roughness • Glove/hairnet audit  • Interactive timers • Strict allergy safeguards
  • Health score gauge • Shelf-life days   • Compliance grading   • Hands-free Q&A     • Grocery list generator
```

---

## 📋 Track Template Deliverables Mapping (8 Categories)

| Category Folder | Included Deliverables (.pdf) | Status |
|---|---|:---:|
| **1. Brainstorming & Ideation** | • `Define Problem Statements .pdf`<br>• `Brainstorming & Idea Prioritization.pdf`<br>• `Empathy Map.pdf` | ✅ Completed |
| **2. Requirement Analysis** | • `Customer Journey Map.pdf`<br>• `Data Flow Diagram.pdf`<br>• `Solution Requirements.pdf`<br>• `Technology Stack.pdf` | ✅ Completed |
| **3. Project Design Phase** | • `Problem-Solution Fit.pdf`<br>• `Proposed Solution.pdf`<br>• `Solution Architecture.pdf` | ✅ Completed |
| **4. Project Planning Phase** | • `Project Planning.pdf` (Milestones 1 to 6) | ✅ Completed |
| **5. Project Development Phase** | • `Coding & Solution.pdf`<br>• `Code-Layout, Readability and Reusability.pdf`<br>• `No. of Functional Features Included in the Solution.pdf`<br>• `backend/` & `frontend/` Source Code | ✅ Completed |
| **6. Project Testing** | • `Performance Testing.pdf` (9/9 Edge Case Test Suite) | ✅ Completed |
| **7. Project Documentation** | • `Project Executable Files.pdf`<br>• `Sample Project Documentation.pdf` | ✅ Completed |
| **8. Project Demonstration** | • `Communication.pdf`<br>• `Demonstration of Proposed Features.pdf`<br>• `Project Demo Planning.pdf`<br>• `Scalability & Future Plan.pdf`<br>• `Team Involvement in Demonstration.pdf` | ✅ Completed |

---

## 🛠️ Tech Stack

| Domain | Technologies |
|---|---|
| **Frontend** | React 18, Vite 6, Modern CSS Variables, Canvas Image Synthesizer, Web Audio MediaRecorder API |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2, Python-Multipart |
| **Computer Vision** | OpenCV (`opencv-python-headless`), Pillow, NumPy, Scikit-Learn |
| **Deep Learning & AI** | Groq Cloud AI (`qwen/qwen3.8-27b` Multimodal Vision & Reasoning, `whisper-large-v3-turbo`), OpenAI |
| **Audio Processing** | SpeechRecognition, Pydub |
| **Testing** | FastAPI TestClient, Automated 9-Point Edge Case Validation Suite |

---

## 🚀 Live Cloud Demo & Quick Start

### 🌐 Instant Live Web App (No Installation Needed)
Access the live production deployment from any browser:  
👉 **[https://foodverse-ai-six.vercel.app/](https://foodverse-ai-six.vercel.app/)**

### 💻 Local Run (1-Click Run)

#### Windows
Double-click [`start_foodverse.bat`](start_foodverse.bat) in the project root.

#### macOS & Linux
```bash
chmod +x start_foodverse.sh
./start_foodverse.sh
```

* **Local Web Application:** [http://localhost:5173](http://localhost:5173)
* **Local API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Automated Testing & Edge-Case Validation

Run the automated test suite anytime:
```bash
cd backend
python test_edge_cases.py
```

```text
============================================================
  FOODVERSE AI - EDGE CASE & ROBUSTNESS VALIDATION SUITE
============================================================

[Module 1: Food Recognition & Nutrition]
  [PASS] Handled tiny 32x32 low-resolution image gracefully.
  [PASS] Correctly rejected empty request with HTTP 400.

[Module 2: Freshness & Spoilage Detection]
  [PASS] Overexposed image processed without crashing (Score: 96).
  [PASS] Correctly rejected 0-byte corrupted image with HTTP 400.

[Module 3: Restaurant Hygiene & Safety]
  [PASS] Dim lighting analyzed cleanly (Score: 70, Grade: Grade B).

[Module 4: Smart Kitchen Cooking Assistant]
  [PASS] Handled minimal/unusual ingredients safely.
  [PASS] Blank culinary query rejected with HTTP 400.

[Module 5: Personalized Meal Planner]
  [PASS] Multi-allergen Vegan plan generated (Target: 1200 kcal).
         Allergens Excluded: peanuts, tree_nuts, gluten, soy, dairy, shellfish.
  [PASS] Out-of-bounds user profile rejected with HTTP 422 Unprocessable Entity.

============================================================
  TEST RESULTS: 9/9 EDGE CASE TESTS PASSED (100% SUCCESS)
============================================================
```

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check & API telemetry status |
| `POST` | `/api/food-recognition/analyze` | Food image detection, audio transcription & macro analysis |
| `POST` | `/api/freshness-detector/analyze` | Computer vision feature extraction & spoilage classification |
| `POST` | `/api/hygiene-monitor/audit` | Video/image frame extraction & kitchen safety score |
| `POST` | `/api/kitchen-assistant/generate-recipe` | Contextual procedural recipe generation |
| `POST` | `/api/kitchen-assistant/ask-assistant` | Live cooking Q&A assistant |
| `POST` | `/api/meal-planner/profile` | Ingest user metrics & compute BMR/TDEE targets |
| `POST` | `/api/meal-planner/generate-plan` | Adaptive meal plan generation with strict allergy safeguards |

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).

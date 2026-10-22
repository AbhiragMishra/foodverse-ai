@echo off
title FoodVerse AI - Launching Platform
echo ========================================================
echo         Launching FoodVerse AI (Backend + Frontend)
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "FoodVerse Backend API" cmd /k "cd /d "%~dp0backend" && .\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "FoodVerse React Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================================
echo FoodVerse AI is live!
echo Web Application: http://localhost:5173
echo API Swagger Docs: http://localhost:8000/docs
echo ========================================================
pause

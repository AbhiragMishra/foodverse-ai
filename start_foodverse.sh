#!/usr/bin/env bash
# FoodVerse AI - Unified Launcher for Linux & macOS

echo "========================================================"
echo "         Launching FoodVerse AI (Backend + Frontend)"
echo "========================================================"
echo ""

# Navigate to script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "[1/2] Starting FastAPI Backend on http://localhost:8000 ..."
cd "$DIR/backend"
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "[2/2] Starting React Frontend on http://localhost:5173 ..."
cd "$DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================================"
echo "FoodVerse AI is running!"
echo "Web Application: http://localhost:5173"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop both servers."
echo "========================================================"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait

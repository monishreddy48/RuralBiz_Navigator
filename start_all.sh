#!/usr/bin/env bash
# RuralBiz Navigator - Linux / macOS Launcher

echo "========================================================"
echo "  RuralBiz Navigator -- Next.js + FastAPI Launcher"
echo "  SIH 2026 Problem Statement SIH26091 / PS 91"
echo "========================================================"
echo ""

echo "[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..."
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "[2/2] Starting Next.js Frontend on http://localhost:3000 ..."
cd frontend && npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

echo ""
echo "Servers running:"
echo "  - Web App:      http://localhost:3000"
echo "  - API Swagger:  http://127.0.0.1:8000/docs"
echo ""

wait


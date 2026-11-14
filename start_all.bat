@echo off
title RuralBiz Navigator - Full-Stack Launcher
echo ========================================================
echo   RuralBiz Navigator -- Next.js + FastAPI Launcher
echo   SIH 2026 Problem Statement SIH26091 / PS 91
echo ========================================================
echo.

echo [1/2] Starting Python FastAPI Backend on http://127.0.0.1:8000 ...
start "RuralBiz Backend (FastAPI)" cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Next.js Frontend on http://localhost:3000 ...
start "RuralBiz Frontend (Next.js)" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are launching!
echo   - Web Platform:  http://localhost:3000
echo   - Backend Docs:  http://127.0.0.1:8000/docs
echo.
timeout /t 3 >nul
start http://localhost:3000


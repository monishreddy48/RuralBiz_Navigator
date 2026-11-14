# RuralBiz Navigator - PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Green
Write-Host "  RuralBiz Navigator -- Next.js + FastAPI Launcher" -ForegroundColor Green
Write-Host "  SIH 2026 Problem Statement SIH26091 / PS 91" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Starting Next.js Frontend on http://localhost:3000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Start-Sleep -Seconds 3
Write-Host ""
Write-Host "Servers started successfully:" -ForegroundColor Green
Write-Host "  - Web App:      http://localhost:3000" -ForegroundColor Yellow
Write-Host "  - API Swagger:  http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host ""

Start-Process "http://localhost:3000"


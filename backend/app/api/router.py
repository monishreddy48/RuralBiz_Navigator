"""
Unified API v1 Router aggregating all domain sub-routers.
"""
from fastapi import APIRouter
from backend.app.api.feasibility import router as feasibility_router
from backend.app.api.financial import router as financial_router
from backend.app.api.market import router as market_router
from backend.app.api.schemes import router as schemes_router
from backend.app.api.simulator import router as simulator_router
from backend.app.api.alternatives import router as alternatives_router
from backend.app.api.ai import router as ai_router
from backend.app.api.voice import router as voice_router
from backend.app.api.reports import router as reports_router
from backend.app.api.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(feasibility_router)
api_router.include_router(financial_router)
api_router.include_router(market_router)
api_router.include_router(schemes_router)
api_router.include_router(simulator_router)
api_router.include_router(alternatives_router)
api_router.include_router(ai_router)
api_router.include_router(voice_router)
api_router.include_router(reports_router)


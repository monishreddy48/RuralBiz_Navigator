"""
FastAPI Router for AI Advisory Assistant
"""
from fastapi import APIRouter
from backend.app.models.market import AIChatRequest, AIChatResponse
from backend.app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI Advisory Assistant"])

@router.post("/chat", response_model=AIChatResponse)
async def chat_advisory(req: AIChatRequest):
    answer, provider_name = ai_service.ask(
        prompt=req.question,
        context=req.context or {},
        language=req.language
    )
    return AIChatResponse(
        answer=answer,
        provider=provider_name,
        language=req.language
    )


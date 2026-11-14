"""
RuralBiz Navigator - AI Provider Router
Automatically detects available credentials and selects the optimal AI engine.
Defaults to MockProvider (Demo Mode) when no API keys are present.
"""
import logging
from typing import Dict, Any, Tuple
from ai.base_provider import BaseAIProvider
from ai.groq_provider import GroqProvider
from ai.openai_provider import OpenAIProvider
from ai.gemini_provider import GeminiProvider
from ai.mock_provider import MockProvider
from config import DEFAULT_AI_PROVIDER

logger = logging.getLogger(__name__)

def get_active_provider() -> Tuple[BaseAIProvider, str]:
    """
    Selects provider according to priority:
    1. Configured DEFAULT_AI_PROVIDER if available
    2. Groq (if GROQ_API_KEY is present)
    3. Gemini (if GEMINI_API_KEY is present)
    4. OpenAI (if OPENAI_API_KEY is present)
    5. MockProvider (Always available, 100% offline fallback)
    
    Returns (provider_instance, status_display_string)
    """
    preferred = DEFAULT_AI_PROVIDER.lower()
    
    if preferred == "groq":
        gp = GroqProvider()
        if gp.is_available():
            return gp, f"AI Assistant: {gp.get_provider_name()}"
    elif preferred == "openai":
        op = OpenAIProvider()
        if op.is_available():
            return op, f"AI Assistant: {op.get_provider_name()}"
    elif preferred == "gemini":
        gm = GeminiProvider()
        if gm.is_available():
            return gm, f"AI Assistant: {gm.get_provider_name()}"
    elif preferred == "mock":
        return MockProvider(), "AI Assistant: Demo Mode"

    # Auto discovery
    gp = GroqProvider()
    if gp.is_available():
        return gp, f"AI Assistant: {gp.get_provider_name()}"
        
    gm = GeminiProvider()
    if gm.is_available():
        return gm, f"AI Assistant: {gm.get_provider_name()}"

    op = OpenAIProvider()
    if op.is_available():
        return op, f"AI Assistant: {op.get_provider_name()}"

    # Safe deterministic fallback
    return MockProvider(), "AI Assistant: Demo Mode"

def ask_advisory_assistant(
    prompt: str,
    context: Dict[str, Any],
    language: str = "en"
) -> Tuple[str, str]:
    """
    Routes query to the active provider.
    If the remote provider fails, falls back to MockProvider gracefully.
    Returns (response_text, provider_status)
    """
    provider, status = get_active_provider()
    
    try:
        response = provider.generate_response(prompt, context, language)
        return response, status
    except Exception as e:
        logger.warning(f"Active provider {provider.get_provider_name()} failed ({e}); falling back to Demo Engine.")
        mock = MockProvider()
        fallback_resp = mock.generate_response(prompt, context, language)
        return fallback_resp, "AI Assistant: Demo Mode (Fallback)"

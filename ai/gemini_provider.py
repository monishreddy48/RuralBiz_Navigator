"""
RuralBiz Navigator - Gemini Provider
"""
import requests
import json
import logging
from typing import Dict, Any
from ai.base_provider import BaseAIProvider
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = "gemini-1.5-flash"

    def get_provider_name(self) -> str:
        return "Google Gemini (1.5 Flash)"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate_response(
        self,
        prompt: str,
        context: Dict[str, Any],
        language: str = "en"
    ) -> str:
        if not self.is_available():
            raise ValueError("Gemini API key not configured")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        system_instruction = (
            "You are RuralBiz Navigator's expert business advisory assistant for rural micro-entrepreneurs in India. "
            "CRITICAL: Do NOT calculate or guess financial numbers. All math has already been calculated deterministically. "
            "Always structure response as:\n"
            "ANSWER:\n"
            "WHY:\n"
            "EVIDENCE:\n"
            "FINANCIAL IMPACT:\n"
            "RISK:\n"
            "NEXT STEP:\n"
            f"Respond clearly in {language} language."
        )

        content = f"{system_instruction}\n\nContext Facts:\n{json.dumps(context, indent=2)}\n\nUser Question:\n{prompt}"

        payload = {
            "contents": [{
                "parts": [{"text": content}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }

        try:
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.warning(f"Gemini API returned {resp.status_code}: {resp.text}")
                raise RuntimeError(f"Gemini API error {resp.status_code}")
        except Exception as e:
            logger.error(f"Gemini call failed: {e}")
            raise

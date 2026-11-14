"""
RuralBiz Navigator - OpenAI Provider
"""
import requests
import json
import logging
from typing import Dict, Any
from ai.base_provider import BaseAIProvider
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = "gpt-4o-mini"
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def get_provider_name(self) -> str:
        return "OpenAI (GPT-4o-mini)"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate_response(
        self,
        prompt: str,
        context: Dict[str, Any],
        language: str = "en"
    ) -> str:
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")

        system_instruction = (
            "You are RuralBiz Navigator's expert business advisory assistant for rural micro-entrepreneurs in India. "
            "CRITICAL: Do NOT compute mathematical formulas. All math is pre-calculated deterministically. "
            "Use the provided context facts strictly. "
            "Always structure response as:\n"
            "ANSWER:\n"
            "WHY:\n"
            "EVIDENCE:\n"
            "FINANCIAL IMPACT:\n"
            "RISK:\n"
            "NEXT STEP:\n"
            f"Respond clearly in {language} language."
        )

        user_content = f"Context:\n{json.dumps(context, indent=2)}\n\nUser Question:\n{prompt}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }

        try:
            resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.warning(f"OpenAI error {resp.status_code}: {resp.text}")
                raise RuntimeError(f"OpenAI API error {resp.status_code}")
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            raise

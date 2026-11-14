"""
RuralBiz Navigator - AI Advisory Service
Implements Gemini 3.8 Flash LLM integration with deterministic fallback.
"""
import os
import json
import logging
from typing import Dict, Any, Tuple
import requests
from backend.app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.gemini_key = GEMINI_API_KEY
        self.gemini_model = "gemini-3.8-flash"

    def ask(self, prompt: str, context: Dict[str, Any] = None, language: str = "en") -> Tuple[str, str]:
        """
        Processes advisory queries.
        Returns: (answer_text, provider_name)
        """
        context = context or {}
        
        # 1. Attempt Gemini 3.8 Flash if key configured
        if self.gemini_key and len(self.gemini_key.strip()) > 5:
            try:
                answer = self._call_gemini(prompt, context, language)
                return answer, "Google Gemini 3.8 Flash"
            except Exception as e:
                logger.warning(f"Gemini API invocation failed ({e}). Falling back to deterministic local advisor.")
                
        # 2. Deterministic Local Mock Provider
        answer = self._mock_advisory(prompt, context, language)
        return answer, "Demo Engine (Offline Local Advisor)"

    def _call_gemini(self, prompt: str, context: Dict[str, Any], language: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_key}"
        
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
            "contents": [{"parts": [{"text": content}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }
        
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise RuntimeError(f"Gemini HTTP {resp.status_code}: {resp.text}")

    def _mock_advisory(self, prompt: str, context: Dict[str, Any], language: str) -> str:
        p_lower = prompt.lower()
        loc_name = context.get("locality_name", "your selected village")
        biz_name = context.get("business_name", "your selected business")
        score = context.get("viability_score", 78)
        recommendation = context.get("recommendation", "GO")
        emi = context.get("monthly_emi", 3500)
        profit = context.get("monthly_profit", 18500)
        dscr = context.get("dscr", 1.45)
        loan_amount = context.get("loan_amount", 50000)
        scheme_matches = context.get("matched_schemes", ["PMEGP", "PM MUDRA"])

        if any(w in p_lower for w in ["why", "score", "recommend", "decision"]):
            return (
                f"**ANSWER:** {biz_name} is recommended with a viability score of {score}/100 (**{recommendation}**).\n\n"
                f"**WHY:** Strong local demand profile in {loc_name} combined with safe debt coverage ratio (DSCR {dscr:.2f}).\n\n"
                f"**EVIDENCE:** Demographic catchment indicates high customer concentration with limited direct competition.\n\n"
                f"**FINANCIAL IMPACT:** Estimated net monthly surplus of ₹{profit:,.0f} after servicing monthly loan EMI.\n\n"
                f"**RISK:** Local agricultural seasonality and raw material input price fluctuations.\n\n"
                f"**NEXT STEP:** Run the What-If stress test for volume shocks and prepare subsidy documents for {', '.join(scheme_matches[:2])}."
            )
        elif any(w in p_lower for w in ["emi", "loan", "repay"]):
            return (
                f"**ANSWER:** For a loan of ₹{loan_amount:,.0f}, your monthly reducing-balance EMI will be approximately ₹{emi:,.0f}.\n\n"
                f"**WHY:** Structured over a 60-month tenure at standard 9.5% commercial MSME rates with a 3-month moratorium buffer.\n\n"
                f"**EVIDENCE:** DSCR stands at {dscr:.2f}, indicating healthy cash buffer exceeding the commercial lender benchmark of 1.20.\n\n"
                f"**FINANCIAL IMPACT:** Operating cash flows cover EMI {dscr:.2f} times over, leaving ₹{profit:,.0f} net surplus.\n\n"
                f"**RISK:** Missing payments during post-harvest dry months.\n\n"
                f"**NEXT STEP:** Review the month-by-month amortization schedule in the Financial Planning section."
            )
        else:
            return (
                f"**ANSWER:** RuralBiz Navigator has evaluated {biz_name} in {loc_name} with an overall viability rating of {score}/100.\n\n"
                f"**WHY:** The catchment supports steady demand while capital requirements align with your savings.\n\n"
                f"**EVIDENCE:** Mapped 5-10 km radius demonstrates favorable demand-to-competition ratio.\n\n"
                f"**FINANCIAL IMPACT:** Projected monthly net surplus after loan EMI is ₹{profit:,.0f}.\n\n"
                f"**RISK:** Initial customer adoption delay during months 1-3.\n\n"
                f"**NEXT STEP:** Explore matching government schemes like PMEGP (up to 35% subsidy) or download the full bankable DPR."
            )

ai_service = AIService()


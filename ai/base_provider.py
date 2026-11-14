"""
RuralBiz Navigator - AI Provider Base Interface
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAIProvider(ABC):
    """Abstract base class for all AI advisory providers."""
    
    @abstractmethod
    def generate_response(
        self,
        prompt: str,
        context: Dict[str, Any],
        language: str = "en"
    ) -> str:
        """
        Generate grounded advisory response given user prompt, calculation context, and language.
        Must return structured text: ANSWER, WHY, EVIDENCE, FINANCIAL IMPACT, RISK, NEXT STEP.
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return human-readable provider name."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Return True if credentials and dependencies are available."""
        pass

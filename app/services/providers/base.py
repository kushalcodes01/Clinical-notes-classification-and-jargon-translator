from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseLLMProvider(ABC):
    """
    Abstract Base Class for LLM Providers.
    Ensures that MockProvider, GeminiProvider, or any future provider
    implements a uniform interface for all Prompt Engineering tasks.
    """

    @abstractmethod
    def generate_summary(self, clinical_note: str) -> Dict[str, Any]:
        """
        Generate a patient-friendly layperson summary of the clinical note.
        """
        pass

    @abstractmethod
    def translate_jargon(self, clinical_note: str) -> List[Dict[str, Any]]:
        """
        Extract medical jargon and return plain-English definitions and context.
        """
        pass

    @abstractmethod
    def extract_entities(self, clinical_note: str) -> Dict[str, Any]:
        """
        Extract structured entities (symptoms, diagnoses, medications, tests, follow-ups).
        """
        pass

    @abstractmethod
    def run_comparison(self, clinical_note: str) -> Dict[str, Any]:
        """
        Run both Naive and Structured prompts on the same note for A/B comparison.
        """
        pass

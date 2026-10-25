import os
from typing import Dict, Any, List
from app.services.providers.base import BaseLLMProvider
from app.services.providers.mock_provider import MockProvider
from app.services.providers.gemini_provider import GeminiProvider

def get_provider(provider_type: str = None) -> BaseLLMProvider:
    """
    Factory function to retrieve the configured LLM provider.
    Defaults to 'mock' if LLM_PROVIDER is not specified or if GEMINI_API_KEY is absent.
    """
    chosen = (provider_type or os.getenv("LLM_PROVIDER", "mock")).strip().lower()

    if chosen == "gemini":
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not gemini_key:
            # Safe automatic fallback to mock provider with a warning
            print("[LLM_SERVICE] Warning: GEMINI_API_KEY not configured. Falling back to MockProvider.")
            return MockProvider()
        try:
            return GeminiProvider(api_key=gemini_key)
        except Exception as e:
            print(f"[LLM_SERVICE] Error initializing GeminiProvider: {e}. Falling back to MockProvider.")
            return MockProvider()

    # Default fallback is always MockProvider for offline safety & viva reliability
    return MockProvider()

def summarize_clinical_note(clinical_note: str, provider_type: str = None) -> Dict[str, Any]:
    provider = get_provider(provider_type)
    return provider.generate_summary(clinical_note)

def translate_clinical_jargon(clinical_note: str, provider_type: str = None) -> List[Dict[str, Any]]:
    provider = get_provider(provider_type)
    return provider.translate_jargon(clinical_note)

def extract_clinical_entities(clinical_note: str, provider_type: str = None) -> Dict[str, Any]:
    provider = get_provider(provider_type)
    return provider.extract_entities(clinical_note)

def compare_clinical_prompts(clinical_note: str, provider_type: str = None) -> Dict[str, Any]:
    provider = get_provider(provider_type)
    return provider.run_comparison(clinical_note)

def process_all_tasks(clinical_note: str, provider_type: str = None) -> Dict[str, Any]:
    """
    Executes all three core Prompt Engineering tasks (Summarisation,
    Jargon Translation, and Entity Extraction) and bundles them into
    a unified response payload for the frontend.
    """
    provider = get_provider(provider_type)
    summary_data = provider.generate_summary(clinical_note)
    translations = provider.translate_jargon(clinical_note)
    entities = provider.extract_entities(clinical_note)

    return {
        "status": "success",
        "provider": provider.provider_name,
        "summary": summary_data["summary_markdown"],
        "prompt_framework": summary_data.get("prompt_framework", "RCTCO Framework"),
        "translations": translations,
        "entities": entities
    }

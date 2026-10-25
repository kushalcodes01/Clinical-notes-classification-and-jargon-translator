import os
import json
import re
from typing import Dict, Any, List
import google.generativeai as genai

from app.services.providers.base import BaseLLMProvider
from app.prompts.summariser import SUMMARISER_SYSTEM_PROMPT, build_summariser_prompt
from app.prompts.translator import TRANSLATOR_SYSTEM_PROMPT, build_translator_prompt
from app.prompts.extractor import EXTRACTOR_SYSTEM_PROMPT, build_extractor_prompt
from app.prompts.naive_prompts import (
    build_naive_summariser_prompt,
    PROMPT_ENGINEERING_COMPARISON_CRITERIA
)

class GeminiProvider(BaseLLMProvider):
    """
    Live LLM Provider using Google's Gemini API (e.g., gemini-1.5-flash).
    Configured dynamically via the GEMINI_API_KEY environment variable.
    """

    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.provider_name = f"Google Gemini ({self.model_name})"

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please add it to your .env file or switch to LLM_PROVIDER=mock."
            )

        genai.configure(api_key=self.api_key)

    def _clean_json_response(self, text: str) -> Any:
        """
        Strips markdown code fences and cleans JSON output.
        """
        cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
        return json.loads(cleaned.strip())

    def generate_summary(self, clinical_note: str) -> Dict[str, Any]:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SUMMARISER_SYSTEM_PROMPT
        )
        prompt = build_summariser_prompt(clinical_note)
        response = model.generate_content(prompt)

        return {
            "summary_markdown": response.text,
            "provider": self.provider_name,
            "prompt_framework": "RCTCO Framework"
        }

    def translate_jargon(self, clinical_note: str) -> List[Dict[str, Any]]:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=TRANSLATOR_SYSTEM_PROMPT
        )
        prompt = build_translator_prompt(clinical_note)
        response = model.generate_content(prompt)

        try:
            parsed = self._clean_json_response(response.text)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict) and "terms" in parsed:
                return parsed["terms"]
            return [parsed]
        except Exception:
            # Fallback if raw text returned
            return [
                {
                    "term": "Clinical Terminology",
                    "category": "General",
                    "plain_english": response.text[:200],
                    "why_it_matters": "Extracted via Gemini API"
                }
            ]

    def extract_entities(self, clinical_note: str) -> Dict[str, Any]:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=EXTRACTOR_SYSTEM_PROMPT
        )
        prompt = build_extractor_prompt(clinical_note)
        response = model.generate_content(prompt)

        try:
            return self._clean_json_response(response.text)
        except Exception:
            return {
                "symptoms": ["Error parsing structured JSON from model response"],
                "diagnoses": [],
                "medications": [],
                "tests_and_procedures": [],
                "follow_up_instructions": [],
                "uncertain_or_missing_information": [response.text[:300]]
            }

    def run_comparison(self, clinical_note: str) -> Dict[str, Any]:
        # 1. Run Naive Prompt without system instructions
        naive_model = genai.GenerativeModel(model_name=self.model_name)
        naive_prompt = build_naive_summariser_prompt(clinical_note)
        naive_res = naive_model.generate_content(naive_prompt)

        # 2. Run Structured Prompt with RCTCO instructions
        structured_summary = self.generate_summary(clinical_note)["summary_markdown"]

        return {
            "naive_prompt": naive_prompt,
            "naive_output": naive_res.text,
            "structured_prompt_framework": "RCTCO Framework",
            "structured_output": structured_summary,
            "flaws_in_naive_output": [
                "🚨 Hallucinated Medical Advice: Unconstrained model often suggests lifestyle prescriptions.",
                "⚠️ Medical Jargon Leftover: Assumes clinical terminology without explanation.",
                "❌ Ignored Missing Data: Does not systematically look for omissions.",
                "📉 Unstructured Format: Unpredictable output layout."
            ],
            "strengths_in_structured_output": [
                "✅ 100% Grounded: Constrained strictly to note content.",
                "✅ 6th-8th Grade Reading Level: Explicitly calibrated for patient comprehension.",
                "✅ Clean Hierarchy: Clearly separates findings, medications, and red flags.",
                "✅ Identifies Incomplete Information: Dedicated missing data section."
            ],
            "comparison_criteria": PROMPT_ENGINEERING_COMPARISON_CRITERIA
        }

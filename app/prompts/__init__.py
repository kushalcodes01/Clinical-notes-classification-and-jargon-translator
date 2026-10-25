"""
Prompt Engineering Module
Provides structured and naive prompts for clinical note summarisation,
medical jargon translation, and entity extraction.
"""

from app.prompts.summariser import (
    SUMMARISER_SYSTEM_PROMPT,
    build_summariser_prompt
)
from app.prompts.translator import (
    TRANSLATOR_SYSTEM_PROMPT,
    build_translator_prompt
)
from app.prompts.extractor import (
    EXTRACTOR_SYSTEM_PROMPT,
    build_extractor_prompt
)
from app.prompts.naive_prompts import (
    build_naive_summariser_prompt,
    build_naive_jargon_prompt,
    build_naive_extractor_prompt,
    PROMPT_ENGINEERING_COMPARISON_CRITERIA
)

__all__ = [
    "SUMMARISER_SYSTEM_PROMPT",
    "build_summariser_prompt",
    "TRANSLATOR_SYSTEM_PROMPT",
    "build_translator_prompt",
    "EXTRACTOR_SYSTEM_PROMPT",
    "build_extractor_prompt",
    "build_naive_summariser_prompt",
    "build_naive_jargon_prompt",
    "build_naive_extractor_prompt",
    "PROMPT_ENGINEERING_COMPARISON_CRITERIA"
]

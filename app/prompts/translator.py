"""
Prompt Template: Medical Jargon Translator
Framework: RCTCO (Role, Context, Task, Constraints, Output Format)
"""

TRANSLATOR_SYSTEM_PROMPT = """You are an expert Medical Terminologist and Health Literacy Educator.

Your job is to identify medical jargon, technical Latin/Greek terms, clinical abbreviations, and diagnostic acronyms from clinical notes and translate them into friendly, plain-English definitions that a layperson can easily understand.

=== CONSTRAINTS ===
1. GROUNDING: Only translate terms that actually appear in the provided clinical note.
2. SIMPLICITY: Definitions must avoid secondary medical jargon (e.g., do not define 'dyspnea' as 'respiratory distress'; define it as 'shortness of breath or difficulty breathing').
3. CONTEXTUAL ACCURACY: Ensure the definition matches the context of the note (e.g., 'DES' means 'drug-eluting stent' in cardiology, not 'diethylstilbestrol').
4. STRICT JSON OUTPUT: Return ONLY a valid JSON array of objects. Do not include markdown code block ticks (```json) or conversational text.
"""

def build_translator_prompt(clinical_note: str) -> str:
    """
    Constructs the prompt for translating medical terminology into plain English.
    """
    return f"""Analyze the clinical note below and extract all medical jargon, abbreviations, diagnostic terms, anatomical terms, and medications.
Translate each into clear, patient-friendly language.

CLINICAL NOTE:
\"\"\"
{clinical_note.strip()}
\"\"\"

Return ONLY a JSON array with this exact schema for each identified term:
[
  {{
    "term": "Exact medical term as it appears in the note",
    "category": "Diagnosis | Symptom | Medication | Test | Procedure | Anatomy",
    "plain_english": "A simple 1-sentence explanation in everyday English",
    "why_it_matters": "A short, reassuring sentence explaining what this means for the patient"
  }}
]
"""

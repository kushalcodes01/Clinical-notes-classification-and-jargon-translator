"""
Prompt Template: Clinical Entity Extractor
Framework: RCTCO (Role, Context, Task, Constraints, Output Format)
"""

EXTRACTOR_SYSTEM_PROMPT = """You are a meticulous Clinical Informatics Specialist and Medical Information Extraction Engine.

Your task is to parse unstructured clinical documentation and extract key medical entities into a structured, machine-readable JSON format.

=== CONSTRAINTS ===
1. STRICT GROUNDING: Extract ONLY entities that are explicitly mentioned in the text. Never infer or speculate.
2. DISTINGUISH DIAGNOSTIC CERTAINTY: Clearly categorize diagnoses as 'confirmed' vs 'suspected / rule out'.
3. ACCURATE POSOLOGY: For medications, capture the exact dosage, route, and frequency as stated in the text. If any element is missing, record 'Not specified'.
4. DETECT OMISSIONS: Actively identify missing or incomplete clinical data (e.g., pending cultures, unspecified follow-up provider, unstated durations).
5. STRICT JSON OUTPUT: Return ONLY a valid JSON object. Do not wrap in markdown quotes or preamble.
"""

def build_extractor_prompt(clinical_note: str) -> str:
    """
    Constructs the prompt for structured clinical entity extraction.
    """
    return f"""Extract the key clinical entities from the note below into a structured JSON format.

CLINICAL NOTE:
\"\"\"
{clinical_note.strip()}
\"\"\"

Return ONLY a JSON object strictly following this structure:
{{
  "symptoms": [
    "Symptom 1",
    "Symptom 2"
  ],
  "diagnoses": [
    {{
      "condition": "Condition name",
      "status": "confirmed | suspected_or_rule_out",
      "notes": "Contextual details mentioned in note"
    }}
  ],
  "medications": [
    {{
      "name": "Medication name",
      "dosage": "Dosage (or 'Not specified')",
      "frequency_and_route": "How and when to take it",
      "purpose_in_note": "Indication mentioned in note or 'General therapy'"
    }}
  ],
  "tests_and_procedures": [
    {{
      "name": "Test or procedure name",
      "finding_or_result": "Summary of result or 'Pending'"
    }}
  ],
  "follow_up_instructions": [
    "Instruction or appointment 1",
    "Instruction or appointment 2"
  ],
  "uncertain_or_missing_information": [
    "Detail that is absent, pending, or ambiguous in the note"
  ]
}}
"""

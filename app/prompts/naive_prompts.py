"""
Naive (Baseline) Prompts for A/B Prompt Engineering Comparison
Demonstrates common pitfalls: lack of role, absence of grounding constraints,
uncontrolled reading level, and unpredictable output formatting.
"""

def build_naive_summariser_prompt(clinical_note: str) -> str:
    """
    Naive baseline prompt: lacks system role, safety constraints,
    reading-level instructions, or structured sectioning.
    """
    return f"Summarize this doctor's note for a patient:\n\n{clinical_note}"

def build_naive_jargon_prompt(clinical_note: str) -> str:
    """
    Naive baseline prompt for jargon translation: lacks JSON schema,
    category classification, or patient-context grounding.
    """
    return f"Explain the difficult words in this medical note:\n\n{clinical_note}"

def build_naive_extractor_prompt(clinical_note: str) -> str:
    """
    Naive baseline prompt for entity extraction: lacks schema enforcement,
    certainty categorization, or missing-info detection.
    """
    return f"List the symptoms, diagnoses, medications, and follow ups from this note:\n\n{clinical_note}"

# Academic Comparison Metadata for viva defense and evaluation
PROMPT_ENGINEERING_COMPARISON_CRITERIA = [
    {
        "dimension": "Role & Persona (R)",
        "naive_approach": "None specified. The LLM defaults to an unpredictable assistant persona, often alternating between robotic clinical prose and overly casual remarks.",
        "structured_approach": "Explicit persona as a 'Patient Health Literacy Specialist & Clinical Nurse Educator', setting a compassionate, clear, yet clinically rigorous standard."
    },
    {
        "dimension": "Context & Target Audience (C)",
        "naive_approach": "Generic 'for a patient' without specifying education level, health anxiety context, or reading comprehension benchmarks.",
        "structured_approach": "Strictly calibrated to a 6th-to-8th grade reading level with short sentences (under 20 words) and everyday analogies."
    },
    {
        "dimension": "Safety & Anti-Hallucination Constraints (C)",
        "naive_approach": "No grounding rules. The LLM frequently invents unverified medical advice (e.g., 'drink 8 glasses of water', 'avoid fatty foods', or 'you should consult an oncologist').",
        "structured_approach": "Explicit Zero-Extrapolation constraint: strictly limits statements to verified facts in the text. Forbids unauthorized medical prescribing or prognosticating."
    },
    {
        "dimension": "Handling Missing or Ambiguous Data (C)",
        "naive_approach": "Silently ignores gaps or fills them in with assumptions (hallucinations).",
        "structured_approach": "Mandates an explicit 'Missing or Incomplete Information' section flagging absent doctor names, unstated dosages, or pending tests."
    },
    {
        "dimension": "Output Schema & Machine Readability (O)",
        "naive_approach": "Unformatted paragraph stream or inconsistent markdown bullets. Cannot be reliably parsed by frontend UI elements.",
        "structured_approach": "Enforces strict JSON schema or standardized Markdown headers, enabling interactive UI features like hover tooltips, badges, and tables."
    }
]

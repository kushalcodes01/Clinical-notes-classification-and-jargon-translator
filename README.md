# 🩺 Clinical Note Summariser & Jargon Translator Using LLM Models

> **Coursework Project:** Prompt Engineering (BTech Computer Science)  
> **Framework:** RCTCO (Role, Context, Task, Constraints, Output Format)  
> **Backend:** Python / Flask &bull; **Frontend:** Vanilla HTML5, CSS3, JavaScript  
> **Providers:** Built-in Mock Mode (100% Offline Safe) &amp; Google Gemini API (`gemini-1.5-flash`)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](#)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask&logoColor=white)](#)
[![Prompt Engineering](https://img.shields.io/badge/Prompt_Engineering-RCTCO_Framework-0284c7)](#)
[![Safety Guardrails](https://img.shields.io/badge/Clinical_Grounding-Zero_Extrapolation-10b981)](#)

---

## 📌 Executive Summary

Clinical documentation—such as hospital discharge summaries and encounter notes—is authored using specialized Latin roots, diagnostic abbreviations, and shorthand intended for healthcare professionals. Studies in health literacy show that **up to 80% of patients forget or misunderstand their post-visit instructions**, leading to poor medication compliance and unnecessary readmissions.

Generic LLMs (like standard chatbots) often fail when summarizing clinical text: they hallucinate unauthorized lifestyle advice, leave critical jargon unexplained, and silently ignore missing clinical details.

This project implements an **academic Prompt Engineering pipeline** adhering to the **RCTCO Framework** (Role, Context, Task, Constraints, and Output Format). It bridges the health communication gap while guaranteeing **strict zero-extrapolation clinical grounding**.

---

## ✨ Key Features

1. **📑 Layperson Clinical Summariser:**
   - Translates dense clinical encounter notes into an empathetic summary calibrated to a **6th-to-8th grade reading level**.
   - Structured into 4 distinct sections: *What Happened (Overview)*, *What The Doctors Found*, *Medications Prescribed*, and *Emergency Red Flags*.

2. **📖 Medical Jargon Translator:**
   - Automatically detects diagnostic acronyms (*NSTEMI, PCI, DES, CAP, COPD*), symptoms (*dyspnea, diaphoresis, scotoma*), and medications.
   - Provides plain-English definitions and a dedicated *"Why it matters for the patient"* explanation.
   - Interactive search and category filtering in the UI.

3. **🧬 Structured Clinical Entity Extraction:**
   - Extracts factual entities into a strict, validated schema: Symptoms, Confirmed vs. Suspected Diagnoses, Medications with exact posology (dosages, routes, frequencies), Diagnostic tests, and Follow-up appointments.
   - **⚠️ Missing Information Detection:** Explicitly flags unstated physician names, pending cultures, or omitted dates rather than inferring them.

4. **🔬 A/B Prompt Engineering Comparison Lab:**
   - Side-by-side evaluation between a **Baseline Naive Prompt** (*"Summarize this doctor's note"*) and our **Structured RCTCO Prompt**.
   - Directly demonstrates how naive prompts hallucinate unverified medical advice and leave jargon unexplained.

5. **📁 Full CSV Dataset Support:**
   - **Upload CSV:** Drag or select any `.csv` file containing clinical notes.
   - **Record Selector:** Dropdown to switch between dataset rows seamlessly.
   - **Sample CSV:** 1-click download of a preloaded 5-case synthetic clinical dataset.
   - **Export CSV:** Downloads a structured evaluation report containing the original note, plain summary, translated glossary, extracted medications, and missing data flags.

6. **🛡️ Clinical Safety & Ethics:**
   - Prominent, persistent **Educational Prototype Disclaimer**.
   - **100% Synthetic / De-identified Data Only:** Uses synthetic records to respect patient privacy.
   - Strict negative prompts prohibiting unsolicited diagnosing or treatment prescriptions.

---

## 📐 Prompt Engineering Architecture: The RCTCO Framework

Rather than using basic prompts, all system directives in [`app/prompts/`](app/prompts/) implement the **RCTCO Framework**:

```
 ┌───────────────────────────────────────────────────────────────┐
 │                       RCTCO Framework                         │
 ├─────────────────┬─────────────────────────────────────────────┤
 │ Role (R)        │ Expert Patient Health Literacy Specialist   │
 │ Context (C)     │ Anxious patient; 6th–8th grade reading level │
 │ Task (T)        │ Task decomposition: Summary, Jargon, Schema │
 │ Constraints (C) │ ZERO extrapolation, no advice, flag missing │
 │ Output (O)      │ Standardized Markdown & Strict JSON schema  │
 └─────────────────┴─────────────────────────────────────────────┘
```

### Prompt Decomposition:
- [`app/prompts/summariser.py`](app/prompts/summariser.py): Layperson summarisation with 20-word sentence caps and visual markdown sections.
- [`app/prompts/translator.py`](app/prompts/translator.py): Extracts terminology into a JSON array categorized by Diagnosis, Symptom, Medication, Procedure, and Test.
- [`app/prompts/extractor.py`](app/prompts/extractor.py): JSON-constrained entity extraction with certainty categorization (`confirmed` vs `suspected`).
- [`app/prompts/naive_prompts.py`](app/prompts/naive_prompts.py): Baseline naive prompts and academic rubric comparison matrix.

---

## 🏗️ System Architecture

```
                          ┌─────────────────────────┐
                          │   Client Web Browser    │
                          │ (Vanilla HTML / CSS / JS│
                          └────────────┬────────────┘
                                       │ REST API (JSON)
                                       ▼
                          ┌─────────────────────────┐
                          │      Flask Backend      │
                          │     (app/routes.py)     │
                          └────────────┬────────────┘
                                       │
                                       ▼
                          ┌─────────────────────────┐
                          │    LLM Service Router   │
                          │(services/llm_service.py)│
                          └─────┬─────────────┬─────┘
                                │             │
            ┌───────────────────▼─┐         ┌─▼──────────────────┐
            │    Mock Provider    │         │  Gemini Provider   │
            │(100% Offline Safety)│         │(gemini-1.5-flash)  │
            └─────────────────────┘         └────────────────────┘
```

The application uses the **Strategy Pattern** via [`BaseLLMProvider`](app/services/providers/base.py). Switching between offline mock demonstrations and live LLM APIs requires no changes to application routes.

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.
- Git (optional, for version control).

### 1. Clone or Open the Repository
```bash
git clone https://github.com/your-username/clinical-note-summariser.git
cd clinical-note-summariser
```

### 2. Set Up a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration (`.env`)
By default, the application runs in **Mock Mode** (no API key required).

To enable Google Gemini (optional):
1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your free Gemini API key:
   ```ini
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
*(Get a free API key at [Google AI Studio](https://aistudio.google.com/)).*

---

## 💻 Running the Application

Start the local development server:
```powershell
# Windows
.\venv\Scripts\python run.py

# macOS / Linux
python run.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Testing & Evaluation

### 1. Built-in Synthetic Test Cases
The application includes three preloaded clinical cases covering distinct specialties:
- **Case 1 (Cardiology):** Acute Coronary Syndrome (NSTEMI) discharge summary with catheterization, drug-eluting stent (DES), and dual antiplatelet therapy.
- **Case 2 (Neurology):** Outpatient clinical encounter for intractable migraine with scintillating scotoma visual aura and medication overuse headache.
- **Case 3 (Pulmonology):** Community-Acquired Pneumonia (CAP) with COPD flare-up, alveolar consolidation on CXR, and respiratory failure.

### 2. Testing with Custom CSV Files
1. Click **"⬇️ Sample CSV"** on the toolbar to download [`app/data/sample_clinical_notes.csv`](app/data/sample_clinical_notes.csv).
2. Click **"📁 Upload CSV"** and select any `.csv` file.
3. Use the record selector dropdown to switch between patients.
4. Click **"✨ Run Full Pipeline"** to process the note.
5. Click **"📥 Export CSV"** to save your structured evaluation report.

---

## 📂 Project Directory Structure

```
prompt-project/
├── .env.example               # Configuration template
├── .gitignore                 # Excludes venv, cache, logs, and secrets
├── requirements.txt           # Dependency manifest
├── run.py                     # Application entry point
├── README.md                  # Project documentation
├── app/
│   ├── __init__.py            # Flask application factory
│   ├── routes.py              # REST API routes (/process-all, /compare, /sample-csv)
│   ├── data/
│   │   ├── synthetic_notes.json      # 3 preloaded clinical test cases
│   │   └── sample_clinical_notes.csv # 5-case CSV dataset for batch testing
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── summariser.py      # Layperson summary prompt (RCTCO)
│   │   ├── translator.py      # Jargon translation prompt (JSON array)
│   │   ├── extractor.py       # Entity extraction prompt (JSON schema)
│   │   └── naive_prompts.py   # Baseline naive prompt & comparison criteria
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py     # Provider router and orchestrator
│   │   └── providers/
│   │       ├── base.py        # Abstract Base Class for LLM providers
│   │       ├── mock_provider.py   # 100% offline provider for safe demos
│   │       └── gemini_provider.py # Google Gemini API provider
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Vanilla CSS medical-tech glassmorphism
│   │   └── js/
│   │       └── main.js        # Controller (tabs, CSV upload/export, API)
│   └── templates/
│       └── index.html         # Responsive dual-pane UI
└── docs/
    └── VIVA_CHEATSHEET.md     # 10 examiner Q&A and 5-minute presentation script
```

---

## 🎓 College Presentation & Viva Defense

A complete viva defense preparation guide is located at [`docs/VIVA_CHEATSHEET.md`](docs/VIVA_CHEATSHEET.md), including:
- 30-second elevator pitch.
- The 5-minute live demonstration script.
- Top 10 likely examiner questions with model answers (covering Task Decomposition, Zero-Extrapolation, Readability Benchmarks, and HIPAA compliance).

---

## ⚖️ Ethical & Educational Disclaimer

> **IMPORTANT:** This software is an **academic educational prototype** designed solely for demonstrating Prompt Engineering concepts in Computer Science coursework. It does **not** provide medical advice, diagnostic evaluations, or treatment plans. All clinical documentation included in this repository consists of **purely synthetic, fictional records** and contains no Protected Health Information (PHI). Always consult a qualified, licensed healthcare provider for medical concerns.

---

## 📄 License

This project is released under the **MIT License** for academic and educational use.

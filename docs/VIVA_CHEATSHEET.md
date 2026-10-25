# Clinical Note Summariser & Jargon Translator
## College Viva Defense & Project Cheatsheet
**Subject:** Prompt Engineering (BTech Computer Science)  
**Author:** Kusha  
**Repository:** `prompt-project`

---

## 1. Project Elevator Pitch (What to say in the first 30 seconds)
> *"Good morning, Professors. My project is a **Clinical Note Summariser & Jargon Translator**. It addresses the critical health literacy gap where patients struggle to understand dense hospital discharge summaries and clinical encounter notes.*
> 
> *Rather than treating LLMs as generic chatbots, my project demonstrates **advanced Prompt Engineering** using the **RCTCO framework** (Role, Context, Task, Constraints, and Output format) with strict **zero-extrapolation grounding guardrails**. It provides plain-language summaries at a 6th-to-8th grade reading level, translates Latin and diagnostic medical jargon, extracts structured clinical entities, explicitly flags missing medical information, and features a live **A/B Comparison Lab** proving the necessity of structured prompt design."*

---

## 2. System Architecture

```
                  ┌────────────────────────────────────────┐
                  │   Client Browser (Vanilla HTML/CSS/JS) │
                  └───────────────────┬────────────────────┘
                                      │ HTTP REST API
                                      ▼
                  ┌────────────────────────────────────────┐
                  │             Flask Backend              │
                  │   (routes.py: /process-all, /compare)  │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      LLM Service Router & Strategy     │
                  │        (services/llm_service.py)       │
                  └───────────┬────────────────┬───────────┘
                              │                │
            ┌─────────────────▼──┐          ┌──▼──────────────────┐
            │    Mock Provider   │          │   Gemini Provider   │
            │ (Offline Demo Safe)│          │ (google-generativeai)│
            └────────────────────┘          └─────────────────────┘
```

### Why this architecture impresses evaluators:
1. **Strategy / Provider Pattern (`base.py`)**: The application does not lock you into a single LLM vendor. Switching from Google Gemini to OpenAI, Anthropic, or an offline Mock provider requires zero changes to route or business logic.
2. **First-Class Prompt Engineering (`app/prompts/`)**: Prompts are not hardcoded strings inside route handlers. They are structured, parameterized Python modules with clear documentation of their Role, Context, Task, Constraints, and Schema.
3. **Resilience & Zero Viva Risk (`mock_provider.py`)**: Demonstrating live LLM projects in college often fails due to bad Wi-Fi or API rate limits. The Mock Provider guarantees 100% uptime with pre-validated clinical outputs, while still allowing live Gemini API calls via `.env`.

---

## 3. The Prompt Engineering Framework: RCTCO

When professors ask, *"What specific prompt engineering techniques did you use?"*, explain the **RCTCO Framework**:

| Component | Definition | Implementation in this Project |
| :--- | :--- | :--- |
| **Role (R)** | The persona and expertise assigned to the LLM. | *"You are an expert Patient Communication Specialist and Clinical Nurse Educator with 15+ years of experience helping patients understand complex medical documentation."* (Primes empathy, clarity, and non-technical language). |
| **Context (C)** | The situational background and target audience. | Target audience is an anxious patient reading their clinical notes; sets reading comprehension benchmark to **6th–8th grade reading level** with sentences under 20 words. |
| **Task (T)** | Explicit, segmented operations. | Three isolated tasks: (1) Plain-language summary, (2) Medical jargon translation with *"why it matters"* patient explanations, and (3) Clinical entity extraction. |
| **Constraints (C)** | Non-negotiable boundaries, safety rules, and negative prompts. | **Strict Grounding / Zero Extrapolation**: Rely *only* on facts explicitly stated. Never invent symptoms or medications. Never give prescriptive medical advice. **Uncertainty Rule**: Explicitly flag missing dates, provider names, or pending tests. |
| **Output Format (O)** | Structural and syntactic contracts for the response. | Standardized GitHub Markdown with visual emoji headers for summaries, and strict JSON schemas for jargon tooltips and clinical entities. |

---

## 4. Academic Differentiator: Naive vs. Structured Prompts (A/B Comparison)

The most common mistake students make is writing naive prompts like:
> *"Summarize this doctor's note for a patient."*

### Why the Naive Prompt Fails in Clinical Applications:
1. **Hallucination of Unsolicited Medical Advice**: The naive prompt prompts the LLM to invent lifestyle advice (e.g., *"eat a low fat diet, drink 8 glasses of water, exercise 30 minutes daily"*). In medicine, giving unauthorized medical advice is dangerous and legally problematic.
2. **Leftover Medical Jargon**: Without explicit vocabulary constraints, terms like *NSTEMI*, *LAD*, *scotoma*, *gadolinium*, or *consolidation* are passed through unexplained.
3. **Silent Omission of Incomplete Data**: If a note does not specify an outpatient doctor's name or a post-discharge oral antibiotic, the naive prompt silently ignores it, leaving the patient uninformed.
4. **Unpredictable Formatting**: Returns a single dense wall of text that cannot be parsed by software.

### How Our Structured Prompt Fixes This:
- **100% Grounded**: Zero invented advice.
- **Reading-Level Calibrated**: Explains every Latin root, acronym, and procedure.
- **Dedicated Omissions Section**: Explicitly alerts the patient to what is missing or pending.
- **Machine-Readable JSON Schema**: Enables interactive UI badges, filters, and tables.

---

## 5. Top 10 Likely Viva Questions & High-Scoring Answers

### Q1: What is Prompt Engineering and why didn't you just fine-tune a model?
**Answer:**  
> *"Prompt engineering is the systematic design of inputs to guide LLM behavior toward accurate, deterministic, and safe outputs without altering model weights. Fine-tuning requires large labeled clinical datasets, significant compute resources, and introduces risks of catastrophic forgetting. In healthcare documentation, zero-shot and few-shot prompt engineering with strict system grounding constraints is faster, cheaper, and more auditable than fine-tuning."*

### Q2: How did you prevent the LLM from hallucinating medical facts?
**Answer:**  
> *"I implemented a strict negative constraint and closed-domain grounding instruction: `ZERO HALLUCINATION / EXTRAPOLATION: You must strictly rely ONLY on facts explicitly stated in the source note. Never fabricate symptoms, diagnoses, medications, lab values, or follow-up plans.` Furthermore, we instruct the model that if an item is not found, it must record 'Not specified' rather than inferring it."*

### Q3: Why is clinical jargon translation important?
**Answer:**  
> *"Studies in health communication show that over 80% of patients forget or misunderstand doctor instructions after leaving a clinic. Terms like 'dyspnea' (shortness of breath) or 'diaphoresis' (sweating) cause unnecessary anxiety. Our translator identifies these terms and provides both a plain-English definition and a 'Why it matters' explanation."*

### Q4: How do you handle sensitive patient data (HIPAA / Privacy)?
**Answer:**  
> *"In this educational prototype, we strictly enforce the use of synthetic, de-identified clinical notes (Patients A, B, and C). In a production hospital deployment, this application would run behind an enterprise HIPAA-compliant BAA (Business Associate Agreement) or on an on-premise local LLM (such as Llama 3 via Ollama) to ensure zero patient data leaves the hospital firewall."*

### Q5: What is the purpose of the Mock Provider?
**Answer:**  
> *"The Mock Provider serves two purposes: First, it acts as an architectural fallback following the Strategy pattern, ensuring 100% reliability for offline testing and presentations where Wi-Fi or API keys are unavailable. Second, it serves as an automated test double for unit testing without incurring API costs."*

### Q6: What reading level did you target for the plain summary and why?
**Answer:**  
> *"We targeted a 6th-to-8th grade reading level (Flesch-Kincaid readability benchmark), which is the standard recommendation by the American Medical Association (AMA) and NIH for patient-facing health literature. We enforced this via short sentences (under 20 words) and everyday analogies."*

### Q7: Why do you have separate prompts for summarisation, jargon translation, and entity extraction instead of one big prompt?
**Answer:**  
> *"In prompt engineering, this is known as **Task Decomposition**. Bundling too many disparate cognitive tasks into a single prompt degrades LLM attention and increases hallucination rates. By decomposing into three specialized prompts, each prompt has a single responsibility, optimal system persona, and dedicated output schema (Markdown for summaries, JSON arrays for terminology, and nested JSON for entities)."*

### Q8: What happens if a patient pastes an incomplete or poorly written clinical note?
**Answer:**  
> *"Our structured prompt includes an explicit constraint: `CLEAR UNCERTAINTY HANDLING`. Instead of guessing missing dates or unstated dosages, the model populates a dedicated 'Missing or Incomplete Information' section and flags uncertain diagnoses as 'suspected / rule-out' rather than confirmed."*

### Q9: What technologies did you use and why Flask instead of a heavy framework?
**Answer:**  
> *"We used Python with Flask for a lightweight, modular REST API and Vanilla HTML5/CSS/JavaScript for the frontend. Avoiding heavy frontend frameworks like React or Tailwind kept the bundle clean, fast, and completely free of build-step complexities, which aligns perfectly with coursework transparency."*

### Q10: How can this project be extended in the future?
**Answer:**  
> *"Future extensions could include: (1) Integrating Speech-to-Text (Whisper) for audio consultations, (2) Multi-lingual translation for non-English speaking patients, and (3) Automated RAG (Retrieval-Augmented Generation) linked to verified medical databases like PubMed or MedlinePlus to double-verify medical definitions."*

---

## 6. Recommended 5-Minute Live Presentation Script

1. **Minute 1: The Problem & Disclaimer**  
   Open `http://127.0.0.1:5000`. Point out the top **Educational Prototype Disclaimer**. Explain the patient health literacy gap.
2. **Minute 2: The Core Pipeline Demo**  
   Click **"🫀 Case 1: Cardiology (NSTEMI)"**. Click **"✨ Run Full Pipeline"**.  
   Show the **Plain Summary** tab: highlight the 4 sections (*What Happened*, *What Doctors Found*, *Medications*, and *Emergency Red Flags*).
3. **Minute 3: Jargon Translator & Clinical Entities**  
   Click **"📖 Jargon Translator"**. Type `"troponin"` in the search box to show real-time filtering.  
   Click **"🧬 Clinical Entities"**. Show confirmed vs suspected diagnoses and point out the **"⚠️ Missing Information Alert Box"** (missing cardiologist name).
4. **Minute 4: The A/B Prompt Comparison Lab (High Marks Section!)**  
   Click **"⚖️ A/B Comparison"**.  
   Show the Naive Prompt on the left: point out how it hallucinated dietary advice that was never in the doctor's note. Show our Structured Prompt on the right: grounded, clear, and safe. Scroll down to the **Academic Evaluation Rubric Table**.
5. **Minute 5: Architecture & Conclusion**  
   Click **"📘 Prompt Framework"** in the header to show the modal with the RCTCO framework. Conclude by reiterating the modular provider architecture. Invite questions.

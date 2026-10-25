import re
from typing import Dict, Any, List
from app.services.providers.base import BaseLLMProvider
from app.prompts.naive_prompts import PROMPT_ENGINEERING_COMPARISON_CRITERIA

class MockProvider(BaseLLMProvider):
    """
    Mock LLM Provider for offline demonstrations, testing, and viva defense.
    Provides verified clinical responses for preloaded synthetic cases
    and a dynamic rule-based fallback for custom user-entered notes.
    """

    def __init__(self):
        self.provider_name = "Mock Provider (Offline Demo Mode)"

    def _detect_case(self, note: str) -> str:
        text = note.lower()
        if "myocardial" in text or "troponin" in text or "nstemi" in text or "lad" in text:
            return "case-1"
        elif "migraine" in text or "cephalalgia" in text or "scotoma" in text or "sumatriptan" in text:
            return "case-2"
        elif "pneumonia" in text or "copd" in text or "ceftriaxone" in text or "bronchograms" in text:
            return "case-3"
        return "custom"

    def generate_summary(self, clinical_note: str) -> Dict[str, Any]:
        case = self._detect_case(clinical_note)

        if case == "case-1":
            markdown = (
                "### 🩺 What Happened (Overview)\n"
                "You were brought to the emergency department because of sudden, intense chest pressure that spread into your left arm and jaw, "
                "along with heavy sweating and shortness of breath. Tests confirmed that you experienced a heart attack (specifically an NSTEMI), "
                "caused by a severe 80% narrowing in one of your heart's main arteries.\n\n"
                "### 🔍 What The Doctors Found\n"
                "- **Heart Muscle Stress**: Blood tests showed elevated troponin levels (peaked at 0.82 ng/mL), which is a clear chemical marker indicating temporary heart muscle stress.\n"
                "- **Artery Blockage**: An angiogram (a visual camera check of your blood vessels) identified an 80% blockage in your Left Anterior Descending artery.\n"
                "- **Successful Procedure**: Doctors successfully placed a small mesh tube called a drug-eluting stent (DES) through your wrist artery to keep the vessel open and restore full blood flow.\n"
                "- **Heart Pumping Strength**: An ultrasound of your heart (echocardiogram) showed your overall pumping strength is good (50%), with only mild temporary sluggishness near the blockage area.\n\n"
                "### 💊 Medications You Were Prescribed\n"
                "- **Aspirin (81 mg daily)**: Keeps blood platelets smooth to prevent clots from forming inside your new stent.\n"
                "- **Clopidogrel / Plavix (75 mg daily)**: A second blood-thinner taken together with aspirin (dual therapy) for at least 12 months to protect the stent.\n"
                "- **Atorvastatin (80 mg at bedtime)**: A high-strength cholesterol-lowering pill that stabilizes your blood vessel walls.\n"
                "- **Metoprolol Succinate (25 mg daily)**: A beta-blocker that helps your heart beat at a calm, steady rate and reduces heart workload.\n"
                "- **Nitroglycerin (0.4 mg under the tongue as needed)**: Dissolves rapidly under your tongue to relax heart blood vessels if chest pain returns.\n\n"
                "### 📋 Next Steps & Red Flag Warning Signs\n"
                "- **Follow-up Appointment**: Scheduled at the outpatient Cardiology Clinic in 2 weeks.\n"
                "- **Lab Tests**: Repeat blood and cholesterol panels in 6 weeks.\n"
                "- **Cardiac Rehabilitation**: A referral was submitted for guided, heart-safe exercise training.\n"
                "- **🚨 Emergency Red Flag**: If you feel recurrent chest pressure, take 1 nitroglycerin tablet under your tongue. If the pain does not go away within 5 minutes, call 911 immediately.\n\n"
                "### ⚠️ Missing or Incomplete Information\n"
                "- The specific name of your assigned outpatient cardiologist is not specified in this note.\n\n"
                "### ℹ️ Important Reminder\n"
                "*This plain-language summary was generated for educational purposes to help you understand your doctor's documentation. Always discuss your care plan directly with your healthcare provider.*"
            )
        elif case == "case-2":
            markdown = (
                "### 🩺 What Happened (Overview)\n"
                "You visited the neurology clinic for severe, recurring right-sided throbbing headaches lasting 4 days. "
                "Your headaches are accompanied by visual disturbances (flashing lights and blind spots), intense sensitivity to light and sound, and vomiting. "
                "Over-the-counter pain relievers have stopped working.\n\n"
                "### 🔍 What The Doctors Found\n"
                "- **Diagnosis**: You have intractable migraine with visual aura. This means recurring neurological headaches preceded by temporary visual symptoms.\n"
                "- **Brain Scan (MRI)**: Your MRI brain scan was completely normal. There is no evidence of stroke, bleeding, or brain tumors.\n"
                "- **Medication Overuse Component**: Frequent daily use of over-the-counter pain medications (ibuprofen and acetaminophen/caffeine) has caused 'rebound' headaches.\n\n"
                "### 💊 Medications Prescribed\n"
                "- **Sumatriptan (50 mg at migraine onset)**: A targeted rescue medication that narrows dilated blood vessels during an attack.\n"
                "- **Ondansetron (4 mg dissolvable tablet)**: Taken under the tongue every 8 hours as needed for severe nausea.\n"
                "- **Topiramate (25 mg nightly)**: A daily preventive pill to reduce the frequency and severity of future attacks (gradually titrated).\n"
                "- **Stop OTC Meds**: Stop taking daily over-the-counter pain relievers to break the rebound cycle.\n\n"
                "### 📋 Next Steps & Red Flag Warning Signs\n"
                "- **Headache Diary**: Log daily triggers, sleep, and headache duration for 30 days.\n"
                "- **Follow-up**: Outpatient neurology clinic review in 6 weeks.\n"
                "- **🚨 Red Flag Warning**: Seek emergency evaluation immediately if you experience a sudden 'thunderclap' headache (reaching maximum intensity in seconds) or sudden muscle weakness.\n\n"
                "### ⚠️ Missing or Incomplete Information\n"
                "- Daily sodium and dietary restrictions were not evaluated or documented in this note.\n\n"
                "### ℹ️ Important Reminder\n"
                "*This educational summary helps translate your medical record. Always consult your neurologist for clinical decisions.*"
            )
        elif case == "case-3":
            markdown = (
                "### 🩺 What Happened (Overview)\n"
                "You were admitted to the hospital with a 5-day history of worsening shortness of breath, fever, chills, and a productive cough with thick greenish mucus. "
                "Your oxygen level on room air was low (89%), requiring supplemental oxygen through a nasal tube.\n\n"
                "### 🔍 What The Doctors Found\n"
                "- **Community-Acquired Pneumonia**: A serious bacterial infection in the lower right lobe of your lung.\n"
                "- **COPD Flare-Up**: Your underlying lung condition (COPD) flared up due to the lung infection.\n"
                "- **Lab & X-Ray Findings**: High white blood cell count (15,400) indicating an active immune response, and chest X-ray showing dense consolidation (fluid/infection in the lung air sacs).\n\n"
                "### 💊 Medications Prescribed\n"
                "- **Ceftriaxone (1 g IV daily)**: A broad-spectrum intravenous antibiotic targeting lung bacteria.\n"
                "- **Azithromycin (500 mg IV daily)**: An antibiotic providing atypical respiratory bacterial coverage.\n"
                "- **Duoneb Inhaler/Nebulizer**: Albuterol/Ipratropium breathed in every 6 hours to open up narrowed airways.\n"
                "- **Prednisone (40 mg daily for 5 days)**: A steroid pill to reduce inflammation in your bronchial tubes.\n"
                "- **Supplemental Oxygen**: Kept at 2 Liters to maintain oxygen levels between 90-94% safely.\n\n"
                "### 📋 Next Steps & Red Flag Warning Signs\n"
                "- **Breathing Exercises**: Use the incentive spirometer 10 times every hour while awake.\n"
                "- **Lab Review**: Sputum culture results will be reassessed at 48 hours to confirm the exact antibiotic match.\n"
                "- **Follow-up**: Repeat chest X-ray before discharge and follow up with Pulmonology in 4 weeks.\n\n"
                "### ⚠️ Missing or Incomplete Information\n"
                "- The specific oral antibiotic pill choice for when you go home is pending sputum culture results.\n\n"
                "### ℹ️ Important Reminder\n"
                "*This educational summary is for understanding your hospital note. Speak with your care team for any clinical questions.*"
            )
        else:
            markdown = (
                "### 🩺 What Happened (Overview)\n"
                f"This clinical note documents an evaluation concerning: {clinical_note[:120]}...\n\n"
                "### 🔍 What The Doctors Found\n"
                "- Key clinical observations and test findings were reviewed and documented by the healthcare team.\n"
                "- The findings reflect the specific clinical concerns evaluated during this encounter.\n\n"
                "### 💊 Medications Mentioned\n"
                "- Any medications listed in your note are designated for symptom management or underlying condition therapy.\n\n"
                "### 📋 Next Steps & What To Watch For\n"
                "- Follow up with your healthcare provider as scheduled or if your symptoms worsen.\n\n"
                "### ⚠️ Missing or Incomplete Information\n"
                "- Specific follow-up dates or pending test outcomes should be confirmed directly with your provider's office.\n\n"
                "### ℹ️ Important Reminder\n"
                "*Educational summary generated via Mock Provider. Consult your doctor for medical advice.*"
            )

        return {
            "summary_markdown": markdown,
            "provider": self.provider_name,
            "prompt_framework": "RCTCO (Role, Context, Task, Constraints, Output Format)"
        }

    def translate_jargon(self, clinical_note: str) -> List[Dict[str, Any]]:
        case = self._detect_case(clinical_note)

        if case == "case-1":
            return [
                {
                    "term": "Acute coronary syndrome (ACS)",
                    "category": "Diagnosis",
                    "plain_english": "An umbrella term for situations where blood flow to the heart muscle is suddenly reduced.",
                    "why_it_matters": "Requires immediate hospital care to protect heart muscle tissue."
                },
                {
                    "term": "Non-ST elevation myocardial infarction (NSTEMI)",
                    "category": "Diagnosis",
                    "plain_english": "A type of heart attack where an artery is partially or temporarily blocked, damaging some heart muscle without showing classic ST-elevation spikes on an ECG.",
                    "why_it_matters": "Confirms heart damage occurred but prompt treatment prevents further injury."
                },
                {
                    "term": "Cardiac troponin I",
                    "category": "Test",
                    "plain_english": "A protein released into the bloodstream only when heart muscle cells are stressed or injured.",
                    "why_it_matters": "A rising troponin level proves a heart attack occurred and helps track recovery."
                },
                {
                    "term": "Percutaneous coronary intervention (PCI)",
                    "category": "Procedure",
                    "plain_english": "A minimally invasive procedure where doctors guide a thin catheter into a narrowed heart artery to reopen it.",
                    "why_it_matters": "Restores vital blood and oxygen supply to your heart muscle."
                },
                {
                    "term": "Drug-eluting stent (DES)",
                    "category": "Procedure",
                    "plain_english": "A tiny expandable metal mesh tube coated with medication that stays inside the opened artery.",
                    "why_it_matters": "Scaffolds the artery open while slowly releasing medication to prevent scar tissue blockages."
                },
                {
                    "term": "Substernal / Diaphoresis / Dyspnea",
                    "category": "Symptom",
                    "plain_english": "Substernal means behind the breastbone; diaphoresis means heavy cold sweats; dyspnea means shortness of breath.",
                    "why_it_matters": "These are the classic hallmark warning signals of reduced blood flow to the heart."
                },
                {
                    "term": "Dual antiplatelet therapy (DAPT)",
                    "category": "Medication",
                    "plain_english": "Taking two different blood-thinning pills (Aspirin + Clopidogrel) together.",
                    "why_it_matters": "Critical to prevent blood clots from sticking to the newly placed metal stent."
                }
            ]
        elif case == "case-2":
            return [
                {
                    "term": "Refractory cephalalgia",
                    "category": "Symptom",
                    "plain_english": "A severe headache that does not respond to standard over-the-counter pain medications.",
                    "why_it_matters": "Explains why basic painkillers failed and why specialized prescription treatment is needed."
                },
                {
                    "term": "Scintillating scotoma",
                    "category": "Symptom",
                    "plain_english": "A visual disturbance where a shimmering, jagged, or flickering blind spot appears in your field of vision.",
                    "why_it_matters": "A classic 'aura' warning sign that a migraine attack is beginning."
                },
                {
                    "term": "Homonymous hemianopsia",
                    "category": "Symptom",
                    "plain_english": "A temporary loss of vision in the same half of the visual field in both eyes.",
                    "why_it_matters": "Caused by temporary electrical changes in the visual processing part of the brain during an aura."
                },
                {
                    "term": "Photophobia & Phonophobia",
                    "category": "Symptom",
                    "plain_english": "Extreme sensitivity or pain caused by normal light and sound.",
                    "why_it_matters": "Common migraine symptoms reflecting brain sensory hypersensitivity."
                },
                {
                    "term": "Medication overuse headache (MOH)",
                    "category": "Diagnosis",
                    "plain_english": "Rebound headaches caused by taking acute pain relief medications too frequently.",
                    "why_it_matters": "Stopping daily OTC pain relievers is necessary to stop the headache cycle."
                },
                {
                    "term": "Gadolinium-enhanced MRI",
                    "category": "Test",
                    "plain_english": "A detailed magnetic brain scan using a safe contrast dye to highlight blood vessels and inflammation.",
                    "why_it_matters": "Confirmed that your brain structure is completely healthy and ruled out dangerous conditions."
                }
            ]
        elif case == "case-3":
            return [
                {
                    "term": "Community-acquired pneumonia (CAP)",
                    "category": "Diagnosis",
                    "plain_english": "A lung infection caught during everyday life in the community rather than inside a hospital.",
                    "why_it_matters": "Guides the doctors to prescribe the correct targeted antibiotic combination."
                },
                {
                    "term": "Alveolar consolidation & Air bronchograms",
                    "category": "Test",
                    "plain_english": "The tiny air sacs in your lung have filled with fluid and inflammatory cells instead of air, making airways visible against white cloudy lung tissue on X-ray.",
                    "why_it_matters": "Direct visual proof of active pneumonia on your chest X-ray."
                },
                {
                    "term": "Leukocytosis with left shift",
                    "category": "Test",
                    "plain_english": "A high white blood cell count with an increased number of immature immune cells (bands).",
                    "why_it_matters": "Demonstrates your body's bone marrow is vigorously fighting off an acute bacterial infection."
                },
                {
                    "term": "Hypoxemic respiratory failure",
                    "category": "Diagnosis",
                    "plain_english": "Blood oxygen level falling below safe limits (here 89%), making it harder for oxygen to reach vital organs.",
                    "why_it_matters": "Explains why supplemental oxygen therapy via nasal tube is required."
                },
                {
                    "term": "Incentive spirometry",
                    "category": "Procedure",
                    "plain_english": "A handheld breathing exercise device with a plastic chamber that measures deep inhalations.",
                    "why_it_matters": "Helps re-expand collapsed lung sacs and clears trapped mucus to prevent complications."
                }
            ]
        else:
            # Fallback heuristic
            return [
                {
                    "term": "Clinical Encounter",
                    "category": "General",
                    "plain_english": "A formal documented visit between a patient and a medical provider.",
                    "why_it_matters": "Serves as the legal and medical record of your care."
                },
                {
                    "term": "Differential Diagnosis",
                    "category": "Diagnosis",
                    "plain_english": "A list of possible conditions the doctor considers before reaching a final diagnosis.",
                    "why_it_matters": "Helps rule out serious illnesses through focused testing."
                }
            ]

    def extract_entities(self, clinical_note: str) -> Dict[str, Any]:
        case = self._detect_case(clinical_note)

        if case == "case-1":
            return {
                "symptoms": [
                    "Acute substernal chest pressure radiating to left shoulder and jaw",
                    "Diaphoresis (heavy sweating)",
                    "Dyspnea on minimal exertion (shortness of breath)"
                ],
                "diagnoses": [
                    {
                        "condition": "Non-ST elevation myocardial infarction (NSTEMI)",
                        "status": "confirmed",
                        "notes": "Supported by peak troponin I of 0.82 ng/mL and ST depressions in leads V4-V6"
                    },
                    {
                        "condition": "Acute coronary syndrome (ACS)",
                        "status": "confirmed",
                        "notes": "Presentation condition upon ED arrival"
                    },
                    {
                        "condition": "Coronary artery disease (CAD) with 80% mid-LAD stenosis",
                        "status": "confirmed",
                        "notes": "Visualized during coronary angiography"
                    }
                ],
                "medications": [
                    {
                        "name": "Aspirin",
                        "dosage": "81 mg",
                        "frequency_and_route": "PO (by mouth) daily",
                        "purpose_in_note": "Antiplatelet therapy (lifetime)"
                    },
                    {
                        "name": "Clopidogrel",
                        "dosage": "75 mg",
                        "frequency_and_route": "PO (by mouth) daily",
                        "purpose_in_note": "Dual antiplatelet therapy (minimum 12 months for DES)"
                    },
                    {
                        "name": "Atorvastatin",
                        "dosage": "80 mg",
                        "frequency_and_route": "PO (by mouth) at bedtime (qhs)",
                        "purpose_in_note": "High-intensity lipid-lowering therapy"
                    },
                    {
                        "name": "Metoprolol succinate",
                        "dosage": "25 mg",
                        "frequency_and_route": "PO (by mouth) daily",
                        "purpose_in_note": "Rate control, target resting HR 60-70 bpm"
                    },
                    {
                        "name": "Nitroglycerin",
                        "dosage": "0.4 mg",
                        "frequency_and_route": "Sublingual (under the tongue) PRN (as needed)",
                        "purpose_in_note": "Recurrent chest pain relief"
                    }
                ],
                "tests_and_procedures": [
                    {
                        "name": "Serial cardiac troponin I",
                        "finding_or_result": "Initial 0.04 ng/mL, peaked at 0.82 ng/mL at 6 hours"
                    },
                    {
                        "name": "12-lead ECG",
                        "finding_or_result": "1.5mm ST depressions and T-wave inversions in leads V4-V6"
                    },
                    {
                        "name": "Echocardiogram",
                        "finding_or_result": "LVEF 50% with mild anterolateral wall hypokinesis"
                    },
                    {
                        "name": "Coronary Angiography",
                        "finding_or_result": "80% stenosis in mid-LAD artery"
                    },
                    {
                        "name": "Percutaneous Coronary Intervention (PCI)",
                        "finding_or_result": "Single drug-eluting stent (DES) deployed successfully via right radial artery"
                    }
                ],
                "follow_up_instructions": [
                    "Cardiology outpatient clinic visit in 2 weeks",
                    "Repeat comprehensive metabolic panel (CMP) and lipid panel in 6 weeks",
                    "Cardiac rehabilitation enrollment referral placed",
                    "Seek immediate emergency care if chest pain persists >5 minutes after 1 nitroglycerin tablet"
                ],
                "uncertain_or_missing_information": [
                    "Specific outpatient cardiologist physician name not designated in note",
                    "Specific appointment time and clinic location address not stated"
                ]
            }
        elif case == "case-2":
            return {
                "symptoms": [
                    "Right-sided pulsatile cephalalgia (8/10 on pain scale) for 4 days",
                    "Scintillating scotomas (flickering visual aura)",
                    "Transient left homonymous hemianopsia (30 min duration)",
                    "Severe photophobia and phonophobia",
                    "Intractable nausea and two episodes of bilious vomiting"
                ],
                "diagnoses": [
                    {
                        "condition": "Intractable episodic migraine with typical visual aura",
                        "status": "confirmed",
                        "notes": "Without status migrainosus"
                    },
                    {
                        "condition": "Medication overuse headache component",
                        "status": "confirmed",
                        "notes": "Secondary to daily use of OTC NSAIDs and acetaminophen/caffeine"
                    }
                ],
                "medications": [
                    {
                        "name": "Sumatriptan",
                        "dosage": "50 mg",
                        "frequency_and_route": "PO at onset of headache, repeat once after 2 hours if needed (max 200mg/24h)",
                        "purpose_in_note": "Acute migraine abortive therapy"
                    },
                    {
                        "name": "Ondansetron",
                        "dosage": "4 mg",
                        "frequency_and_route": "ODT (oral disintegrating tablet) PRN every 8 hours",
                        "purpose_in_note": "Nausea / emesis control"
                    },
                    {
                        "name": "Topiramate",
                        "dosage": "25 mg (titrate weekly to 50 mg BID)",
                        "frequency_and_route": "PO daily at bedtime",
                        "purpose_in_note": "Preventive migraine therapy"
                    }
                ],
                "tests_and_procedures": [
                    {
                        "name": "Neurological physical exam",
                        "finding_or_result": "Cranial nerves II-XII intact, fundoscopy normal, no papilledema, Romberg negative"
                    },
                    {
                        "name": "Brain MRI with/without gadolinium",
                        "finding_or_result": "Normal brain parenchyma; no hemorrhage, mass lesion, or abnormal enhancement"
                    }
                ],
                "follow_up_instructions": [
                    "Maintain daily headache symptom and trigger diary for 30 days",
                    "Return to neurology clinic in 6 weeks",
                    "Discontinue daily OTC combined analgesics",
                    "Seek emergency evaluation for thunderclap headache or focal deficits"
                ],
                "uncertain_or_missing_information": [
                    "Specific daily sodium or dietary restrictions were not evaluated or documented"
                ]
            }
        elif case == "case-3":
            return {
                "symptoms": [
                    "Progressive dyspnea (shortness of breath) for 5 days",
                    "Chills and nocturnal diaphoresis",
                    "Productive cough yielding thick purulent greenish sputum",
                    "Right-sided pleuritic chest pain aggravated by deep breathing"
                ],
                "diagnoses": [
                    {
                        "condition": "Community-acquired bacterial pneumonia (CAP)",
                        "status": "confirmed",
                        "notes": "CURB-65 score = 2 (tachypneic, age >= 65)"
                    },
                    {
                        "condition": "Acute exacerbation of COPD (AECOPD)",
                        "status": "confirmed",
                        "notes": "Triggered by acute pulmonary infection"
                    },
                    {
                        "condition": "Mild hypoxemic respiratory insufficiency",
                        "status": "confirmed",
                        "notes": "Oxygen-responsive (SpO2 89% ambient -> 94% on 2L NC)"
                    }
                ],
                "medications": [
                    {
                        "name": "Ceftriaxone",
                        "dosage": "1 g",
                        "frequency_and_route": "IV every 24 hours",
                        "purpose_in_note": "Antibacterial coverage for pneumonia"
                    },
                    {
                        "name": "Azithromycin",
                        "dosage": "500 mg",
                        "frequency_and_route": "IV every 24 hours",
                        "purpose_in_note": "Atypical bacterial coverage"
                    },
                    {
                        "name": "Duoneb (Albuterol / Ipratropium)",
                        "dosage": "2.5 mg / 0.5 mg",
                        "frequency_and_route": "Nebulized every 6 hours PRN",
                        "purpose_in_note": "Bronchodilation for wheezing/dyspnea"
                    },
                    {
                        "name": "Prednisone",
                        "dosage": "40 mg",
                        "frequency_and_route": "PO daily for 5 days",
                        "purpose_in_note": "Anti-inflammatory for COPD flare"
                    }
                ],
                "tests_and_procedures": [
                    {
                        "name": "Complete Blood Count (CBC)",
                        "finding_or_result": "Leukocytosis: WBC 15.4k with 84% neutrophils and left shift (6% bands)"
                    },
                    {
                        "name": "Serum Lactate",
                        "finding_or_result": "1.6 mmol/L (normal)"
                    },
                    {
                        "name": "Sputum Gram Stain & Culture",
                        "finding_or_result": "Gram-positive diplococci (suggestive of S. pneumoniae); final culture pending"
                    },
                    {
                        "name": "Chest Radiograph (CXR)",
                        "finding_or_result": "Dense right lower lobe alveolar consolidation with air bronchograms"
                    }
                ],
                "follow_up_instructions": [
                    "Incentive spirometry 10 breaths every hour while awake",
                    "Reassess sputum culture at 48 hours for antibiotic de-escalation",
                    "Repeat chest radiograph prior to hospital discharge",
                    "Outpatient pulmonology clinic appointment in 4 weeks"
                ],
                "uncertain_or_missing_information": [
                    "Outpatient oral antibiotic step-down choice is pending final culture results"
                ]
            }
        else:
            return {
                "symptoms": ["Documented in note"],
                "diagnoses": [{"condition": "Clinical observation", "status": "reviewed", "notes": "From source text"}],
                "medications": [{"name": "As documented", "dosage": "Per note", "frequency_and_route": "As directed", "purpose_in_note": "Therapy"}],
                "tests_and_procedures": [{"name": "Clinical evaluation", "finding_or_result": "Reviewed in record"}],
                "follow_up_instructions": ["Consult healthcare provider"],
                "uncertain_or_missing_information": ["Review full chart with medical staff"]
            }

    def run_comparison(self, clinical_note: str) -> Dict[str, Any]:
        """
        Generates realistic side-by-side comparison between Naive and Structured prompts.
        """
        case = self._detect_case(clinical_note)

        # Naive response showing real-world flaws
        if case == "case-1":
            naive_output = (
                "The patient had chest pain and sweating and went to the hospital. He had an NSTEMI which is a heart attack. "
                "His troponin was 0.82 and he had an ECG with ST depression. The doctor did a catheterization and put a drug eluting stent in his LAD artery. "
                "He was given Aspirin, Clopidogrel, Atorvastatin, Metoprolol, and Nitroglycerin. He should take his pills and eat a low fat diet, "
                "exercise 30 minutes a day, and reduce stress. Follow up in 2 weeks."
            )
            structured_summary = self.generate_summary(clinical_note)["summary_markdown"]
        elif case == "case-2":
            naive_output = (
                "Patient is a 34 year old female with right sided headache, scintillating scotoma, photophobia, phonophobia, and vomiting. "
                "Her MRI was normal without gadolinium enhancement issues. She has intractable migraine with aura. She should take sumatriptan and ondansetron. "
                "Topiramate was started. Drink plenty of water and get 8 hours of sleep. Return in 6 weeks."
            )
            structured_summary = self.generate_summary(clinical_note)["summary_markdown"]
        else:
            naive_output = (
                "Patient has pneumonia and COPD exacerbation. WBC was 15.4 with left shift. CXR showed consolidation. "
                "Give Ceftriaxone, Azithromycin, Duoneb, and Prednisone. Follow up in 4 weeks."
            )
            structured_summary = self.generate_summary(clinical_note)["summary_markdown"]

        return {
            "naive_prompt": "Summarize this doctor's note for a patient:\n[Clinical Note]",
            "naive_output": naive_output,
            "structured_prompt_framework": "RCTCO Framework (System Persona + 6th Grade Level + Strict Grounding + JSON/Markdown schema)",
            "structured_output": structured_summary,
            "flaws_in_naive_output": [
                "🚨 Hallucinated Medical Advice: Invented dietary/lifestyle prescriptions ('eat low fat diet', 'exercise 30 minutes', 'drink plenty of water') that were NEVER written by the doctor.",
                "⚠️ Medical Jargon Leftover: Failed to explain clinical terms like 'NSTEMI', 'LAD', 'scotoma', 'gadolinium', 'consolidation', or 'left shift'.",
                "❌ Ignored Missing Data: Failed to alert the patient that specific doctor names or oral antibiotic transition plans were absent.",
                "📉 Poor Structure: Lacks emergency red-flag callouts, medication explanations, or readable sectioning."
            ],
            "strengths_in_structured_output": [
                "✅ 100% Grounded: Zero invented advice or hallucinated treatments.",
                "✅ 6th-8th Grade Reading Level: All medical terminology is translated immediately in context.",
                "✅ Clear Visual Hierarchy: Separates overview, findings, medications, and emergency red flags.",
                "✅ Detects Incomplete Information: Explicitly flags missing doctor names or pending lab tests."
            ],
            "comparison_criteria": PROMPT_ENGINEERING_COMPARISON_CRITERIA
        }

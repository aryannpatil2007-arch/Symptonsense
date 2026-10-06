import re
from typing import List, Tuple, Optional

# Clinical Red-Flag Keywords & Symptoms that trigger immediate emergency response
EMERGENCY_SYMPTOM_MAP = {
    "chest_pain": "Severe chest pain or cardiac pressure",
    "chest_pressure_radiating": "Chest pain radiating to left arm, neck, or jaw",
    "slurred_speech": "Sudden slurred or impaired speech (Stroke warning)",
    "facial_weakness": "Sudden facial drooping or one-sided weakness (Stroke warning)",
    "arm_leg_weakness": "Sudden numbness or paralysis on one side of the body",
    "sudden_confusion": "Acute confusion, delirium, or altered mental status",
    "blood_in_sputum": "Hemoptysis (Coughing up frank blood)",
    "sudden_severe_dizziness": "Sudden incapacitating vertigo with loss of balance",
    "loss_of_balance": "Acute ataxia or inability to maintain upright stance",
    "severe_sharp_flank_pain": "Acute intractable renal / flank colic",
    "lower_right_abdominal_pain": "Acute severe right lower quadrant abdominal pain (Appendicitis risk)"
}

EMERGENCY_TEXT_PATTERNS = [
    (r"\b(heart attack|chest pressure|crushing chest|crushing pain)\b", "Severe acute cardiac chest pressure"),
    (r"\b(stroke|face drop|slur|slurred speech|one side numb|arm drift)\b", "Suspected acute stroke symptoms (FAST warning)"),
    (r"\b(can'?t breathe|gasping|severe breathlessness|suffocating|choking)\b", "Critical respiratory compromise"),
    (r"\b(vomiting blood|coughing blood|blood in vomit|black tarry stool)\b", "Active severe gastrointestinal or pulmonary hemorrhage"),
    (r"\b(unconscious|fainted|syncope|passed out|unresponsive)\b", "Loss of consciousness / severe syncopal episode"),
    (r"\b(thunderclap|worst headache of my life|explosive headache)\b", "Thunderclap headache (Intracranial emergency)"),
    (r"\b(anaphylaxis|throat closing|tongue swelling|lip swelling)\b", "Severe acute anaphylactic airway edema")
]

def check_emergency_red_flags(symptoms: List[str], free_text: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Evaluates whether the provided symptoms or free-text narrative indicate
    a life-threatening medical emergency requiring immediate 911/ER attention.
    """
    # 1. Check selected symptoms
    for sym in symptoms:
        clean_sym = sym.strip().lower()
        if clean_sym in EMERGENCY_SYMPTOM_MAP:
            return True, EMERGENCY_SYMPTOM_MAP[clean_sym]
            
    # 2. Check free text description with regex
    if free_text:
        text_lower = free_text.lower()
        for pattern, reason in EMERGENCY_TEXT_PATTERNS:
            if re.search(pattern, text_lower):
                return True, reason
                
    return False, None

def extract_symptoms_from_text(free_text: str, all_symptom_ids: List[str]) -> List[str]:
    """
    Intelligently extracts matching symptom IDs from free-form patient narrative.
    """
    if not free_text:
        return []
        
    extracted = set()
    text_clean = " " + re.sub(r"[^\w\s]", " ", free_text.lower()) + " "
    
    # Custom common conversational aliases to standardized symptom IDs
    aliases = {
        "fever": "fever",
        "high temperature": "high_fever",
        "chills": "chills",
        "cough": "dry_cough",
        "coughing": "dry_cough",
        "productive cough": "productive_cough",
        "phlegm": "phlegm_production",
        "mucus": "phlegm_production",
        "shortness of breath": "shortness_of_breath",
        "breathless": "shortness_of_breath",
        "chest pain": "chest_pain",
        "chest pressure": "chest_pressure_radiating",
        "chest burn": "chest_burning",
        "heartburn": "heartburn",
        "acid reflux": "acid_regurgitation",
        "headache": "throbbing_headache",
        "migraine": "throbbing_headache",
        "sore throat": "sore_throat",
        "throat pain": "sore_throat",
        "runny nose": "runny_nose",
        "blocked nose": "nasal_congestion",
        "congested": "nasal_congestion",
        "sneezing": "sneezing",
        "itchy eyes": "itchy_eyes",
        "watery eyes": "watery_eyes",
        "loss of smell": "loss_of_smell",
        "loss of taste": "loss_of_taste",
        "tired": "fatigue",
        "exhausted": "severe_fatigue",
        "weakness": "muscle_weakness",
        "dizzy": "dizziness",
        "vertigo": "dizziness",
        "nausea": "nausea",
        "throwing up": "vomiting",
        "vomit": "vomiting",
        "diarrhea": "watery_diarrhea",
        "loose motion": "watery_diarrhea",
        "stomach pain": "abdominal_cramping",
        "belly pain": "abdominal_cramping",
        "burning urination": "burning_urination",
        "urine burn": "burning_urination",
        "peeing a lot": "frequent_urination",
        "thirsty": "excessive_thirst",
        "rash": "skin_rash",
        "itchy": "intense_skin_itching",
        "joint pain": "symmetric_joint_pain",
        "big toe pain": "severe_big_toe_joint_pain",
        "slurred speech": "slurred_speech",
        "face drooping": "facial_weakness"
    }
    
    for phrase, sym_id in aliases.items():
        if f" {phrase} " in text_clean:
            if sym_id in all_symptom_ids:
                extracted.add(sym_id)
                
    for sym_id in all_symptom_ids:
        parts = sym_id.split("_")
        joined = " ".join(parts)
        if f" {joined} " in text_clean:
            extracted.add(sym_id)
            
    return sorted(list(extracted))

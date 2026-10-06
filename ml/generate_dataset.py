import json
import os
import random
import numpy as np
import pandas as pd

# Define all 30 Clinical Diseases with detailed symptom profiles and EHR history associations
DISEASE_DEFINITIONS = {
    "Common Cold": {
        "category": "Respiratory",
        "icd10": "J00",
        "urgency": "Low",
        "specialist": "General Physician",
        "description": "Mild viral infection of the upper respiratory tract causing nasal congestion, sneezing, and sore throat.",
        "core_symptoms": ["runny_nose", "nasal_congestion", "sneezing", "sore_throat"],
        "secondary_symptoms": ["mild_cough", "mild_fatigue", "headache", "low_grade_fever", "throat_irritation", "watery_eyes"],
        "rare_symptoms": ["body_aches", "loss_of_appetite"],
        "ehr_associations": {"age_group": "any", "smoker_weight": 1.1},
        "recommended_actions": [
            "Rest adequately and drink plenty of fluids (warm water, herbal teas, broths).",
            "Use OTC saline nasal sprays or decongestants as appropriate for temporary congestion relief.",
            "Consult a physician if symptoms last more than 10-14 days or worsen suddenly."
        ],
        "home_care": ["Steam inhalation 2-3 times daily.", "Warm saltwater gargling.", "Elevate head with pillows while sleeping."],
        "red_flags": ["Difficulty breathing or wheezing", "High fever > 39°C (102°F) lasting > 3 days", "Severe facial sinus pain"]
    },
    "Influenza (Flu)": {
        "category": "Infectious / Respiratory",
        "icd10": "J10.1",
        "urgency": "Medium",
        "specialist": "General Physician / Infectious Disease",
        "description": "Acute contagious viral respiratory infection characterized by sudden high fever, intense muscle aches, and fatigue.",
        "core_symptoms": ["high_fever", "severe_body_aches", "chills", "fatigue"],
        "secondary_symptoms": ["dry_cough", "headache", "sore_throat", "nasal_congestion", "sweating", "loss_of_appetite"],
        "rare_symptoms": ["nausea", "dizziness"],
        "ehr_associations": {"has_asthma": 1.4, "age_over_65": 1.3, "has_diabetes": 1.3},
        "recommended_actions": [
            "Consult doctor within 48h of onset for consideration of prescription antivirals (e.g. Oseltamivir).",
            "Isolate at home to prevent transmission.",
            "Take acetaminophen or ibuprofen for fever/aches (avoid aspirin in young patients)."
        ],
        "home_care": ["Bed rest and continuous electrolyte hydration.", "Warm honey-lemon tea for cough.", "Humidifier in bedroom."],
        "red_flags": ["Shortness of breath or rapid breathing", "Bluish tint around lips/fingernails", "Inability to keep liquids down"]
    },
    "COVID-19": {
        "category": "Infectious / Respiratory",
        "icd10": "U07.1",
        "urgency": "Medium",
        "specialist": "Pulmonologist / General Physician",
        "description": "Viral illness caused by SARS-CoV-2 presenting with respiratory symptoms, fever, and classic loss of smell or taste.",
        "core_symptoms": ["fever", "dry_cough", "loss_of_smell", "loss_of_taste", "fatigue"],
        "secondary_symptoms": ["shortness_of_breath", "body_aches", "sore_throat", "headache", "nasal_congestion", "chills"],
        "rare_symptoms": ["diarrhea", "nausea", "chest_tightness"],
        "ehr_associations": {"has_hypertension": 1.5, "has_diabetes": 1.6, "is_smoker": 1.4, "bmi_high": 1.4, "age_over_65": 1.6},
        "recommended_actions": [
            "Perform a rapid antigen or RT-PCR COVID test immediately.",
            "Isolate and check oxygen saturation (SpO2) every 4-6 hours.",
            "Consult healthcare provider if you have underlying conditions or SpO2 < 95%."
        ],
        "home_care": ["Isolate in well-ventilated room.", "Prone positioning (lying on stomach) to assist lung airflow.", "Hydrate heavily."],
        "red_flags": ["SpO2 oxygen saturation dropping below 94%", "Severe shortness of breath or persistent chest pressure", "Confusion or extreme lethargy"]
    },
    "Bacterial Pneumonia": {
        "category": "Respiratory",
        "icd10": "J18.9",
        "urgency": "High",
        "specialist": "Pulmonologist",
        "description": "Infection inflaming the lungs' alveoli, causing fluid accumulation, productive cough, high fever, and impaired oxygenation.",
        "core_symptoms": ["productive_cough", "phlegm_production", "high_fever", "shortness_of_breath", "chest_pain_on_breathing"],
        "secondary_symptoms": ["chills", "severe_fatigue", "sweating", "loss_of_appetite", "rapid_shallow_breathing"],
        "rare_symptoms": ["confusion_in_elderly", "nausea", "bluish_lips"],
        "ehr_associations": {"is_smoker": 1.8, "has_asthma": 1.6, "age_over_65": 1.8, "has_diabetes": 1.5},
        "recommended_actions": [
            "Seek clinical evaluation with Chest X-ray and sputum/blood tests within 24 hours.",
            "Adhere strictly to full course of prescribed antibiotics.",
            "Emergency room admission if oxygen levels drop or breathing is strained."
        ],
        "home_care": ["Strict rest and warm fluid intake.", "Humidifier use.", "Avoid all tobacco smoke exposure."],
        "red_flags": ["Severe dyspnea or gasping for air", "Coughing up rust-colored or bloody sputum", "Confusion or cyanosis"]
    },
    "Bronchial Asthma": {
        "category": "Respiratory / Allergic",
        "icd10": "J45.9",
        "urgency": "High",
        "specialist": "Pulmonologist / Allergist",
        "description": "Chronic inflammatory airway disease producing reversible airway bronchospasm, wheezing, and breathlessness.",
        "core_symptoms": ["wheezing", "shortness_of_breath", "chest_tightness", "difficulty_breathing_at_night"],
        "secondary_symptoms": ["dry_cough", "rapid_breathing", "throat_irritation", "anxiety_from_breathlessness"],
        "rare_symptoms": ["fatigue", "nasal_congestion"],
        "ehr_associations": {"has_asthma": 3.0, "has_allergies": 2.2, "family_allergies": 1.8, "is_smoker": 1.5},
        "recommended_actions": [
            "Use fast-acting bronchodilator rescue inhaler (Albuterol) immediately (2-4 puffs).",
            "Refer to personal Asthma Action Plan.",
            "If relief is not achieved within 15 minutes, proceed to emergency room."
        ],
        "home_care": ["Sit upright; avoid lying flat.", "Remove known allergens or triggers immediately.", "Pursed-lip controlled breathing."],
        "red_flags": ["Unable to speak full sentences", "Severe retractions of chest wall", "Rescue inhaler provides zero relief"]
    },
    "Hypertension Crisis": {
        "category": "Cardiovascular",
        "icd10": "I10",
        "urgency": "High",
        "specialist": "Cardiologist / General Physician",
        "description": "Marked elevation in systemic blood pressure creating risk for end-organ vascular complications.",
        "core_symptoms": ["headache_morning", "dizziness", "palpitations", "vision_blur"],
        "secondary_symptoms": ["nosebleed", "fatigue", "neck_pain_stiffness", "shortness_of_breath_on_exertion", "facial_flushing"],
        "rare_symptoms": ["anxiety", "nausea"],
        "ehr_associations": {"has_hypertension": 3.5, "high_bp_reading": 3.0, "family_heart_disease": 1.8, "bmi_high": 1.6, "age_over_45": 1.7},
        "recommended_actions": [
            "Measure BP using an upper-arm automated or manual cuff after 5 minutes of quiet rest.",
            "If BP >= 180/120 mmHg, seek immediate medical assessment.",
            "Consult cardiologist for antihypertensive prescription adjustment."
        ],
        "home_care": ["Adopt low-sodium DASH diet.", "30 minutes moderate daily aerobic activity.", "Manage stress and stop smoking."],
        "red_flags": ["Chest pain radiating to arm or jaw", "Sudden weakness or slurred speech (Call 911 / ER immediately)", "Acute visual blackout"]
    },
    "Coronary Artery Disease / Angina": {
        "category": "Cardiovascular / Emergency",
        "icd10": "I25.10",
        "urgency": "Emergency",
        "specialist": "Cardiologist / ER",
        "description": "Critical restriction of cardiac arterial blood flow producing myocardial ischemia and acute chest constriction.",
        "core_symptoms": ["chest_pain", "chest_pressure_radiating", "shortness_of_breath", "cold_sweating"],
        "secondary_symptoms": ["palpitations", "dizziness", "nausea", "unexplained_fatigue", "left_arm_tingling"],
        "rare_symptoms": ["jaw_pain", "upper_back_pain"],
        "ehr_associations": {"has_heart_disease": 3.8, "has_hypertension": 2.2, "has_diabetes": 2.0, "high_cholesterol_reading": 2.5, "is_smoker": 2.0, "age_over_45": 2.2, "family_heart_disease": 2.2},
        "recommended_actions": [
            "CALL EMERGENCY SERVICES (911/112) IMMEDIATELY if experiencing severe chest pressure.",
            "Chew one adult aspirin (325 mg) if not allergic.",
            "Rest completely in seated position while waiting for emergency responders."
        ],
        "home_care": ["No home treatment for active chest pain.", "Post-treatment cardiac rehabilitation.", "Strict adherence to statins and antiplatelet drugs."],
        "red_flags": ["Crushing chest pain radiating to jaw/arm > 5 min", "Diaphoresis (profuse cold sweat) with impending doom", "Loss of consciousness"]
    },
    "Type 2 Diabetes Mellitus": {
        "category": "Metabolic & Endocrine",
        "icd10": "E11.9",
        "urgency": "Medium",
        "specialist": "Endocrinologist",
        "description": "Chronic metabolic disease defined by progressive insulin resistance and persistent elevation of blood glucose.",
        "core_symptoms": ["excessive_thirst", "frequent_urination", "excessive_hunger", "unexplained_weight_loss"],
        "secondary_symptoms": ["chronic_fatigue", "vision_blur", "slow_healing_wounds", "tingling_hands_feet", "dry_itchy_skin"],
        "rare_symptoms": ["frequent_infections", "dizziness_after_meals"],
        "ehr_associations": {"has_diabetes": 4.0, "family_diabetes": 2.5, "high_glucose_reading": 3.5, "bmi_high": 2.2, "age_over_45": 1.8},
        "recommended_actions": [
            "Obtain fasting blood glucose and HbA1c laboratory assessment.",
            "Consult endocrinologist for customized pharmacotherapy (Metformin, SGLT2i, GLP-1, or insulin).",
            "Establish regular retinal and podiatry screening."
        ],
        "home_care": ["Regular capillary glucose monitoring.", "Mediterranean carbohydrate-aware nutrition.", "Daily foot inspection for cuts."],
        "red_flags": ["Fruity breath odor with rapid deep breathing (DKA risk)", "Blood glucose > 300 mg/dL with vomiting", "Infected non-healing ulcers"]
    },
    "GERD (Acid Reflux)": {
        "category": "Gastrointestinal",
        "icd10": "K21.9",
        "urgency": "Low",
        "specialist": "Gastroenterologist",
        "description": "Retrograde flow of gastric acid and pepsin into the esophagus producing mucosal irritation and burning retrosternal sensation.",
        "core_symptoms": ["heartburn", "acid_regurgitation", "upper_abdominal_pain", "chest_burning"],
        "secondary_symptoms": ["sour_taste_in_mouth", "bloating", "chronic_throat_clearing", "dry_cough_night", "difficulty_swallowing_mild"],
        "rare_symptoms": ["hiccups", "nausea"],
        "ehr_associations": {"bmi_high": 1.8, "is_smoker": 1.5, "alcohol_use": 1.6},
        "recommended_actions": [
            "Consult a physician regarding OTC or prescription acid suppression (PPIs or H2 blockers).",
            "Maintain food diary to avoid triggers (fatty foods, chocolate, caffeine, spicy cuisine).",
            "Endoscopy recommended if alarm symptoms or long duration."
        ],
        "home_care": ["Elevate head of bed by 6 inches.", "Avoid lying down for 3 hours after meals.", "Eat smaller, frequent meals."],
        "red_flags": ["Difficulty or painful swallowing (dysphagia)", "Vomiting blood or black coffee-ground material", "Unexplained significant weight loss"]
    },
    "Acute Gastroenteritis": {
        "category": "Gastrointestinal",
        "icd10": "A09",
        "urgency": "Medium",
        "specialist": "General Physician / Gastroenterologist",
        "description": "Infectious gastrointestinal inflammation presenting with acute watery diarrhea, emesis, and abdominal cramps.",
        "core_symptoms": ["watery_diarrhea", "nausea", "vomiting", "abdominal_cramping"],
        "secondary_symptoms": ["low_grade_fever", "loss_of_appetite", "fatigue", "headache", "mild_dehydration"],
        "rare_symptoms": ["muscle_aches", "dizziness_on_standing"],
        "ehr_associations": {"age_group": "any"},
        "recommended_actions": [
            "Initiate immediate oral rehydration therapy with WHO-standard ORS or electrolyte solutions.",
            "Consult doctor if unable to maintain oral hydration for > 24 hours.",
            "Stool examination if bloody or lasting > 3 days."
        ],
        "home_care": ["BRAT diet (Bananas, Rice, Applesauce, Toast).", "Avoid dairy, fatty foods, caffeine, and alcohol.", "Wash hands rigorously with soap."],
        "red_flags": ["Signs of severe dehydration (dry sunken eyes, no urination > 8h, lethargy)", "Blood in stool or vomit", "High fever > 39°C"]
    },
    "Peptic Ulcer Disease": {
        "category": "Gastrointestinal",
        "icd10": "K27.9",
        "urgency": "Medium",
        "specialist": "Gastroenterologist",
        "description": "Erosion of gastric or duodenal mucosa commonly induced by Helicobacter pylori colonization or regular NSAID consumption.",
        "core_symptoms": ["burning_stomach_pain", "pain_worse_between_meals", "feeling_of_fullness", "bloating"],
        "secondary_symptoms": ["belching", "nausea", "heartburn", "loss_of_appetite", "mild_weight_loss"],
        "rare_symptoms": ["fatigue_from_anemia", "vomiting"],
        "ehr_associations": {"is_smoker": 1.7, "alcohol_use": 1.8, "age_over_45": 1.4},
        "recommended_actions": [
            "Consult gastroenterologist for H. pylori testing (urea breath test, stool antigen, or endoscopy).",
            "Complete prescribed PPI and triple-therapy antibiotics if H. pylori is confirmed.",
            "Cease NSAID medications immediately."
        ],
        "home_care": ["Eat regular small meals on schedule.", "Avoid alcohol, spicy seasonings, and tobacco.", "Avoid late night snacking."],
        "red_flags": ["Melena (jet black, tarry, sticky stools)", "Hematemesis (vomiting frank red blood)", "Sudden board-like rigid abdominal pain"]
    },
    "Acute Appendicitis": {
        "category": "Gastrointestinal / Surgical",
        "icd10": "K35.80",
        "urgency": "Emergency",
        "specialist": "General Surgeon / Emergency Dept",
        "description": "Rapid obstruction and inflammation of the appendix with high risk of perforation, requiring emergency appendectomy.",
        "core_symptoms": ["lower_right_abdominal_pain", "nausea", "vomiting", "loss_of_appetite"],
        "secondary_symptoms": ["low_grade_fever", "abdominal_swelling_tenderness", "pain_worse_with_coughing_walking", "inability_to_pass_gas"],
        "rare_symptoms": ["diarrhea_or_constipation", "chills"],
        "ehr_associations": {"age_under_35": 1.5},
        "recommended_actions": [
            "EMERGENCY: Proceed to nearest hospital emergency room without delay.",
            "Do NOT eat, drink, or take laxatives/painkillers before examination.",
            "Ultrasound/CT scan and surgical consult will be performed."
        ],
        "home_care": ["No home treatment permitted; surgical emergency."],
        "red_flags": ["Severe sharp pain localized at right lower quadrant (McBurney's point)", "Rebound abdominal tenderness", "High fever with sudden spreading abdominal rigidity"]
    },
    "Acute Migraine Attack": {
        "category": "Neurological",
        "icd10": "G43.909",
        "urgency": "Medium",
        "specialist": "Neurologist",
        "description": "Recurrent neurovascular headache disorder manifesting as severe throbbing unilateral pain with photophobia and nausea.",
        "core_symptoms": ["throbbing_headache", "unilateral_head_pain", "sensitivity_to_light", "sensitivity_to_sound"],
        "secondary_symptoms": ["nausea", "visual_aura", "dizziness", "scalp_tenderness", "fatigue_post_attack"],
        "rare_symptoms": ["vomiting", "nasal_stuffiness_one_side", "mood_irritability"],
        "ehr_associations": {"family_migraine": 2.8, "has_allergies": 1.4},
        "recommended_actions": [
            "Take prescribed migraine abortive agents (Triptans, Gepants, NSAIDs) as early as possible.",
            "Maintain headache diary noting sleep, food, stress triggers.",
            "Consult neurologist for daily preventive medications if attacks occur > 4 days/month."
        ],
        "home_care": ["Rest in pitch-dark, quiet room with cold compress on forehead.", "Deep rhythmic breathing and quiet hydration.", "Avoid looking at phone/computer screens."],
        "red_flags": ["'Thunderclap' headache peaking in under 60 seconds", "Headache with high fever, neck rigidity, confusion", "First severe headache onset after age 50"]
    },
    "Acute Stroke / TIA": {
        "category": "Neurological / Emergency",
        "icd10": "I63.9",
        "urgency": "Emergency",
        "specialist": "Stroke Neurologist / ER",
        "description": "Sudden focal cerebral ischemia resulting from thrombotic or embolic occlusion of brain vasculature.",
        "core_symptoms": ["facial_weakness", "arm_leg_weakness", "slurred_speech", "sudden_confusion"],
        "secondary_symptoms": ["vision_loss_one_eye", "sudden_severe_dizziness", "loss_of_balance", "numbness_one_side"],
        "rare_symptoms": ["sudden_explosive_headache", "difficulty_swallowing"],
        "ehr_associations": {"has_hypertension": 3.2, "has_diabetes": 2.5, "has_heart_disease": 3.0, "is_smoker": 2.2, "high_cholesterol_reading": 2.2, "age_over_65": 2.8},
        "recommended_actions": [
            "CALL 911 / 112 IMMEDIATELY. Note exact time of symptom onset.",
            "Do NOT administer food, liquids, or aspirin before hospital CT scan.",
            "Thrombolytic / thrombectomy intervention is time-critical within hours."
        ],
        "home_care": ["Keep patient lying safely on side if vomiting; await EMS immediately."],
        "red_flags": ["Face droop, arm drift, slurred speech (F.A.S.T.)", "Sudden hemiplegia (paralysis on one side)", "Sudden complete loss of vision or consciousness"]
    },
    "Urinary Tract Infection (UTI)": {
        "category": "Infectious / Urological",
        "icd10": "N39.0",
        "urgency": "Medium",
        "specialist": "Urologist / General Physician",
        "description": "Bacterial proliferation in the urinary bladder or urethra causing dysuria, frequency, and pelvic discomfort.",
        "core_symptoms": ["burning_urination", "frequent_urination", "urgency_to_urinate", "cloudy_foul_urine"],
        "secondary_symptoms": ["pelvic_pain", "blood_in_urine", "low_back_pressure", "mild_fatigue"],
        "rare_symptoms": ["low_grade_fever", "nausea"],
        "ehr_associations": {"has_diabetes": 1.8},
        "recommended_actions": [
            "Submit midstream urine sample for urinalysis and culture/sensitivity testing.",
            "Commence prescribed targeted antibiotic regimen (e.g. Nitrofurantoin, Fosfomycin).",
            "Complete full antibiotic treatment course."
        ],
        "home_care": ["Hydrate copiously (2.5-3 liters of water per day).", "Urinate immediately when urge is felt.", "Warm heating pad on pelvic area."],
        "red_flags": ["High fever, severe flank/back pain, and shaking chills (Ascending Pyelonephritis)", "Gross hematuria with large clots", "Inability to void urine"]
    },
    "Allergic Rhinitis": {
        "category": "Allergic / Immunology",
        "icd10": "J30.9",
        "urgency": "Low",
        "specialist": "Allergist / ENT",
        "description": "IgE-mediated inflammation of nasal membranes triggered by airborne allergens (pollen, dust mites, dander).",
        "core_symptoms": ["sneezing", "itchy_eyes", "watery_eyes", "runny_nose"],
        "secondary_symptoms": ["nasal_congestion", "itchy_throat", "post_nasal_drip", "allergic_shiners_dark_circles", "fatigue_mild"],
        "rare_symptoms": ["mild_cough", "headache_frontal"],
        "ehr_associations": {"has_allergies": 3.8, "has_asthma": 2.2, "family_allergies": 2.5},
        "recommended_actions": [
            "Utilize non-sedating second-generation oral antihistamines or intranasal steroid sprays.",
            "Consider allergen testing and allergen-specific immunotherapy (AIT).",
            "Monitor daily local pollen forecasts."
        ],
        "home_care": ["Saline nasal rinse using sterile saline solution.", "Run HEPA air filtration unit in bedroom.", "Keep windows closed during high-pollen days."],
        "red_flags": ["Lip, tongue, or throat angioedema (Anaphylaxis risk - Call 911)", "Severe wheezing or respiratory compromise"]
    },
    "Eczema (Atopic Dermatitis)": {
        "category": "Dermatological",
        "icd10": "L20.9",
        "urgency": "Low",
        "specialist": "Dermatologist",
        "description": "Chronic pruritic inflammatory skin disorder associated with epidermal barrier dysfunction and immune hyperreactivity.",
        "core_symptoms": ["intense_skin_itching", "red_dry_skin_patches", "skin_flaking", "cracked_skin"],
        "secondary_symptoms": ["skin_lichenification", "sensitive_raw_skin", "small_raised_bumps", "sleep_disturbance_from_itch"],
        "rare_symptoms": ["crusting_oozing", "skin_warmth"],
        "ehr_associations": {"has_allergies": 3.2, "has_asthma": 2.4, "family_allergies": 2.5},
        "recommended_actions": [
            "Consult dermatologist for prescription topical corticosteroids or calcineurin inhibitors during flare-ups.",
            "Perform allergy patch testing if allergic contact triggers are suspected.",
            "Protect skin barrier with regular heavy emollients."
        ],
        "home_care": ["Apply fragrance-free ceramide cream within 3 minutes of bathing.", "Take brief lukewarm showers; avoid hot water.", "Wear soft, breathable cotton garments."],
        "red_flags": ["Honey-colored crusting or pustules (secondary bacterial staph infection)", "Widespread vesicular eruption with fever (Eczema herpeticum)"]
    },
    "Psoriasis": {
        "category": "Dermatological / Autoimmune",
        "icd10": "L40.0",
        "urgency": "Low",
        "specialist": "Dermatologist",
        "description": "T-cell mediated autoimmune dermatosis featuring hyperproliferation of keratinocytes and thick silvery scaled plaques.",
        "core_symptoms": ["silvery_scaled_skin_plaques", "red_thickened_skin_patches", "dry_cracked_skin", "itching_skin_plaques"],
        "secondary_symptoms": ["pitted_nails", "joint_stiffness", "burning_skin_sensation", "plaques_on_elbows_knees_scalp"],
        "rare_symptoms": ["swollen_finger_joints", "skin_bleeding_on_scratch"],
        "ehr_associations": {"family_autoimmune": 2.5, "is_smoker": 1.6, "bmi_high": 1.5},
        "recommended_actions": [
            "Consult dermatologist for topical vitamin D/corticosteroid combinations, phototherapy, or targeted biologics.",
            "Screen for concomitant Psoriatic Arthritis with a rheumatologist.",
            "Evaluate cardiovascular and metabolic parameters regularly."
        ],
        "home_care": ["Apply thick petroleum or ointment-based moisturizers.", "Short daily sun exposure (10-15 min).", "Avoid skin trauma and stressful triggers."],
        "red_flags": ["Generalized fiery red skin peeling over > 90% body surface (Erythrodermic Psoriasis - ER)", "Severe painful swelling of peripheral joints"]
    },
    "Hypothyroidism": {
        "category": "Metabolic & Endocrine",
        "icd10": "E03.9",
        "urgency": "Medium",
        "specialist": "Endocrinologist",
        "description": "Deficient thyroid hormone secretion leading to generalized systemic hypometabolism and fatigue.",
        "core_symptoms": ["unexplained_weight_gain", "chronic_fatigue", "cold_intolerance", "constipation"],
        "secondary_symptoms": ["dry_skin", "hair_thinning", "depressed_mood", "muscle_weakness", "puffy_face", "slow_heart_rate"],
        "rare_symptoms": ["memory_fog", "hoarseness", "heavy_menstrual_periods"],
        "ehr_associations": {"family_autoimmune": 2.4, "age_over_45": 1.6},
        "recommended_actions": [
            "Check serum TSH and Free T4 levels via blood draw.",
            "Initiate daily morning Levothyroxine replacement therapy.",
            "Repeat thyroid function panel at 6-8 weeks to optimize dosage."
        ],
        "home_care": ["Take medication with water 60 minutes before breakfast.", "Avoid calcium/iron supplements within 4h of thyroid pills.", "High-fiber diet."],
        "red_flags": ["Extreme somnolence, hypothermia, severe edema, confusion (Myxedema coma emergency)"]
    },
    "Hyperthyroidism": {
        "category": "Metabolic & Endocrine",
        "icd10": "E05.90",
        "urgency": "Medium",
        "specialist": "Endocrinologist",
        "description": "Excessive thyroid hormone synthesis causing systemic hypermetabolism, tachycardia, and weight loss.",
        "core_symptoms": ["unexplained_weight_loss", "rapid_heartbeat", "palpitations", "heat_intolerance"],
        "secondary_symptoms": ["nervousness_anxiety", "hand_tremors", "excessive_sweating", "frequent_bowel_movements", "sleep_insomnia", "bulging_eyes"],
        "rare_symptoms": ["muscle_weakness_thighs", "irregular_menses"],
        "ehr_associations": {"family_autoimmune": 2.2},
        "recommended_actions": [
            "Test TSH, Free T3, Free T4, and TRAb antibodies.",
            "Prescription beta-blockers for heart rate stabilization and antithyroid medications (Methimazole).",
            "Consult endocrinologist regarding definitive therapy (radioiodine vs surgery)."
        ],
        "home_care": ["Adequate nutrient-dense caloric intake.", "Avoid high-iodine supplements/kelp.", "Rest and stress management."],
        "red_flags": ["Thyroid storm: high fever, extreme agitation, arrhythmia > 140 bpm, delirium (Emergency!)"]
    },
    "Osteoarthritis": {
        "category": "Musculoskeletal",
        "icd10": "M19.90",
        "urgency": "Low",
        "specialist": "Orthopedic Surgeon / Rheumatologist",
        "description": "Mechanical degenerative joint disorder causing progressive articular cartilage degradation and osteophyte formation.",
        "core_symptoms": ["joint_pain_worse_with_activity", "joint_stiffness_morning_brief", "crepitus_grating_sound", "loss_of_joint_flexibility"],
        "secondary_symptoms": ["bone_spurs_swelling", "joint_tenderness", "mild_effusion", "pain_worse_end_of_day"],
        "rare_symptoms": ["joint_instability", "muscle_wasting_around_joint"],
        "ehr_associations": {"age_over_45": 2.4, "bmi_high": 2.0},
        "recommended_actions": [
            "Physical therapy program focusing on quadriceps and periarticular joint strengthening.",
            "Joint X-rays for grading joint space narrowing.",
            "Topical NSAIDs, oral analgesics, or intra-articular injections as recommended."
        ],
        "home_care": ["Low-impact aerobic exercise (swimming, cycling).", "Weight reduction to decrease joint load.", "Warm packs before activity; cold packs after."],
        "red_flags": ["Single joint becoming acutely fiery red, hot, exquisitely swollen with fever (Septic arthritis emergency)"]
    },
    "Rheumatoid Arthritis": {
        "category": "Musculoskeletal / Autoimmune",
        "icd10": "M06.9",
        "urgency": "Medium",
        "specialist": "Rheumatologist",
        "description": "Systemic autoimmune inflammatory polyarthritis characterized by persistent symmetric synovial inflammation and bony erosions.",
        "core_symptoms": ["symmetric_joint_pain", "morning_joint_stiffness_prolonged", "swollen_warm_joints", "hand_finger_joint_swelling"],
        "secondary_symptoms": ["chronic_fatigue", "low_grade_fever", "rheumatoid_nodules", "loss_of_grip_strength", "appetite_loss"],
        "rare_symptoms": ["dry_eyes_mouth", "chest_pleuritic_pain"],
        "ehr_associations": {"family_autoimmune": 2.8, "is_smoker": 1.6},
        "recommended_actions": [
            "Urgent rheumatologist consultation to start disease-modifying antirheumatic drugs (DMARDs, Methotrexate).",
            "Autoantibody panel: Rheumatoid Factor (RF), Anti-CCP, ESR, and CRP.",
            "Baseline ultrasound/radiographs of hands and feet."
        ],
        "home_care": ["Gentle range-of-motion exercises daily.", "Use ergonomic assistive tools.", "Anti-inflammatory diet rich in Omega-3 fatty acids."],
        "red_flags": ["Severe cervical neck pain or numbness in limbs", "Acutely infected hot solitary joint"]
    },
    "Acute Sinusitis": {
        "category": "Respiratory / ENT",
        "icd10": "J01.90",
        "urgency": "Low",
        "specialist": "ENT Specialist / General Physician",
        "description": "Inflammation of paranasal sinus mucosa leading to sinus ostia obstruction, purulent nasal discharge, and facial pressure.",
        "core_symptoms": ["facial_pain_pressure", "nasal_congestion", "thick_yellow_green_mucus", "headache_worse_bending_forward"],
        "secondary_symptoms": ["toothache_upper_jaw", "reduced_smell", "fatigue", "mild_fever", "bad_breath_halitosis"],
        "rare_symptoms": ["ear_fullness", "cough_worse_at_night"],
        "ehr_associations": {"has_allergies": 1.8, "is_smoker": 1.4},
        "recommended_actions": [
            "Supportive symptomatic care; most cases resolve spontaneously within 7-10 days.",
            "If symptoms exceed 10 days or worsen after initial improvement, consult doctor for antibiotics."
        ],
        "home_care": ["Nasal saline irrigation twice daily.", "Warm facial compresses over sinus cavities.", "Stay well hydrated and use room humidifier."],
        "red_flags": ["Periorbital swelling, redness, or protrusion of eye", "Double vision, severe frontal headache, or stiff neck"]
    },
    "Acute Gout Flare": {
        "category": "Metabolic & Musculoskeletal",
        "icd10": "M10.9",
        "urgency": "Medium",
        "specialist": "Rheumatologist / General Physician",
        "description": "Intensely painful crystal arthropathy caused by monosodium urate precipitation in synovial joints, classically the first metatarsophalangeal joint.",
        "core_symptoms": ["severe_big_toe_joint_pain", "sudden_nighttime_joint_pain", "joint_swelling_intense_redness", "joint_exquisitely_tender_to_touch"],
        "secondary_symptoms": ["warmth_over_joint", "shiny_purplish_skin_over_joint", "limited_joint_mobility", "low_grade_fever"],
        "rare_symptoms": ["tophi_subcutaneous_deposits", "chills"],
        "ehr_associations": {"alcohol_use": 2.2, "bmi_high": 1.8, "has_hypertension": 1.6, "family_gout": 2.2},
        "recommended_actions": [
            "Initiate immediate acute anti-inflammatory agent (Colchicine, high-dose NSAID, or steroid) at first twinge.",
            "Check serum uric acid level 2-4 weeks post-flare.",
            "Evaluate for long-term urate-lowering therapy (Allopurinol, Febuxostat)."
        ],
        "home_care": ["Elevate and rest the affected extremity; avoid weight-bearing.", "Ice application wrapped in cloth.", "Drink > 3 liters water daily; avoid red meat, shellfish, beer."],
        "red_flags": ["Fever with shaking chills and hot joint (Urgent synovial aspirate to rule out Septic Joint)"]
    },
    "Dengue Fever": {
        "category": "Infectious Disease",
        "icd10": "A90",
        "urgency": "High",
        "specialist": "Infectious Disease Specialist",
        "description": "Arboviral illness transmitted by Aedes mosquitoes, featuring severe retro-orbital pain, high fever, and marked myalgia.",
        "core_symptoms": ["high_fever", "severe_pain_behind_eyes", "severe_joint_muscle_aches", "skin_rash"],
        "secondary_symptoms": ["nausea_vomiting", "fatigue", "mild_gum_bleeding", "loss_of_appetite", "headache_frontal"],
        "rare_symptoms": ["petechiae_pinpoint_rash", "flushed_skin"],
        "ehr_associations": {"age_group": "any"},
        "recommended_actions": [
            "Perform Dengue NS1 / IgM-IgG testing and baseline Complete Blood Count (CBC).",
            "Monitor platelet count and hematocrit every 24 hours.",
            "Avoid Aspirin/Ibuprofen/NSAIDs due to hemorrhage risk; use Paracetamol only."
        ],
        "home_care": ["Bed rest and rigorous oral rehydration (ORS, coconut water, fresh juices).", "Mosquito bed net to prevent secondary vectors."],
        "red_flags": ["Severe persistent abdominal pain or intractable vomiting", "Bleeding from gums, nose, or hematemesis", "Restlessness, cold clammy skin, or drop in blood pressure (Dengue Shock)"]
    },
    "Atrial Fibrillation (Arrhythmia)": {
        "category": "Cardiovascular",
        "icd10": "I48.91",
        "urgency": "High",
        "specialist": "Cardiologist / Electrophysiologist",
        "description": "Supraventricular tachyarrhythmia characterized by uncoordinated atrial activation and irregularly irregular ventricular response.",
        "core_symptoms": ["irregular_rapid_heartbeat", "palpitations", "dizziness", "shortness_of_breath_on_exertion"],
        "secondary_symptoms": ["fatigue_unexplained", "chest_fluttering", "lightheadedness", "reduced_exercise_capacity"],
        "rare_symptoms": ["chest_discomfort", "syncope_fainting"],
        "ehr_associations": {"has_hypertension": 2.5, "has_heart_disease": 2.8, "age_over_65": 2.6, "alcohol_use": 1.8},
        "recommended_actions": [
            "Perform immediate 12-lead ECG to capture rhythm.",
            "Cardiology consultation for rate/rhythm control and CHA2DS2-VASc stroke risk assessment.",
            "Prescription anticoagulation (DOACs) if stroke risk is elevated."
        ],
        "home_care": ["Avoid caffeine, energy drinks, and excessive alcohol.", "Daily pulse tracking or smartwatch rhythm monitoring.", "Stress management."],
        "red_flags": ["Chest pain accompanying rapid irregular heart rate", "Fainting or loss of consciousness", "Sudden unilateral neurological weakness (Stroke alert)"]
    },
    "Irritable Bowel Syndrome (IBS)": {
        "category": "Gastrointestinal",
        "icd10": "K58.0",
        "urgency": "Low",
        "specialist": "Gastroenterologist",
        "description": "Functional gastrointestinal disorder characterized by recurrent abdominal pain related to defecation, altered stool frequency or form.",
        "core_symptoms": ["abdominal_pain_relieved_by_defecation", "bloating_abdominal_distension", "alternating_diarrhea_constipation", "mucus_in_stool"],
        "secondary_symptoms": ["gas_flatulence", "feeling_of_incomplete_evacuation", "urgency_for_bowel_movement", "nausea_mild"],
        "rare_symptoms": ["fatigue", "backache"],
        "ehr_associations": {"age_group": "any"},
        "recommended_actions": [
            "Consult gastroenterologist to establish Rome IV criteria and rule out organic disease (Celiac serology, fecal calprotectin).",
            "Consider a structured Low-FODMAP dietary trial with a dietitian.",
            "Use antispasmodics or probiotics as recommended."
        ],
        "home_care": ["Keep a food and symptom diary.", "Gradual soluble fiber intake (Psyllium).", "Regular exercise and stress-reduction therapy."],
        "red_flags": ["Unexplained weight loss or nocturnal diarrhea waking patient from sleep", "Rectal bleeding or blood in stool", "New onset symptoms over age 50"]
    },
    "Tension-Type Headache": {
        "category": "Neurological",
        "icd10": "G44.209",
        "urgency": "Low",
        "specialist": "General Physician / Neurologist",
        "description": "The most common primary headache, presenting with a bilateral dull, non-pulsatile band-like ache around the head and neck.",
        "core_symptoms": ["band_like_headache", "dull_aching_head_pain", "neck_shoulder_muscle_tightness", "scalp_tenderness"],
        "secondary_symptoms": ["mild_fatigue", "difficulty_concentrating", "sensitivity_to_stress", "mild_sound_sensitivity"],
        "rare_symptoms": ["mild_light_sensitivity"],
        "ehr_associations": {"age_group": "any"},
        "recommended_actions": [
            "Manage acute episodes with simple analgesics (Acetaminophen, Ibuprofen); limit usage to < 2-3 days/week to prevent medication overuse headache.",
            "Consult doctor if headaches become chronic (> 15 days/month)."
        ],
        "home_care": ["Warm compress or heating pad on neck and shoulders.", "Ergonomic workspace adjustments.", "Daily neck stretching and relaxation exercises."],
        "red_flags": ["Sudden explosive onset headache", "Headache accompanied by fever, neck stiffness, or motor weakness"]
    },
    "Kidney Stone Disease (Nephrolithiasis)": {
        "category": "Urological / Emergency",
        "icd10": "N20.0",
        "urgency": "High",
        "specialist": "Urologist / Emergency Dept",
        "description": "Hard crystalline mineral deposits formed inside kidneys passing through ureters, triggering severe spasmodic flank colic.",
        "core_symptoms": ["severe_sharp_flank_pain", "pain_radiating_to_groin", "blood_in_urine", "nausea_vomiting"],
        "secondary_symptoms": ["burning_urination", "frequent_urination", "cloudy_urine", "restlessness_inability_to_find_comfortable_position"],
        "rare_symptoms": ["chills_fever", "reduced_urine_output"],
        "ehr_associations": {"family_gout": 1.5, "bmi_high": 1.4},
        "recommended_actions": [
            "Urgent non-contrast CT scan of kidneys, ureters, and bladder (KUB CT) or ultrasound.",
            "Prescription analgesics (NSAIDs/opioids) and alpha-blockers (Tamsulosin) for stone passage.",
            "Urological intervention (ESWL, ureteroscopy) if stone > 6mm or causing obstruction."
        ],
        "home_care": ["Drink 3+ liters of water daily.", "Strain urine with filter to catch stone for chemical analysis.", "Heating pad on flank."],
        "red_flags": ["Fever and chills accompanying renal colic (Infected obstructed kidney - Urological Emergency)", "Total inability to pass urine"]
    },
    "Viral Hepatitis (Acute)": {
        "category": "Gastrointestinal / Infectious",
        "icd10": "B19.9",
        "urgency": "High",
        "specialist": "Gastroenterologist / Hepatologist",
        "description": "Inflammation of the liver tissue most commonly due to viral infection (Hepatitis A, B, C, or E) causing jaundice and hepatic enzyme elevation.",
        "core_symptoms": ["jaundice_yellow_eyes_skin", "dark_tea_colored_urine", "pale_clay_colored_stools", "upper_right_abdominal_pain"],
        "secondary_symptoms": ["severe_fatigue", "loss_of_appetite", "nausea_vomiting", "mild_fever", "generalized_skin_itching"],
        "rare_symptoms": ["joint_aches", "weight_loss"],
        "ehr_associations": {"alcohol_use": 2.0},
        "recommended_actions": [
            "Comprehensive Liver Function Tests (LFTs) and viral hepatitis serology panel (HAV IgM, HBsAg, Anti-HCV, HEV IgM).",
            "Consult hepatologist for monitoring of liver enzymes, coagulopathy (INR), and antiviral therapy if indicated.",
            "Discontinue all hepatotoxic medications and alcohol immediately."
        ],
        "home_care": ["Adequate nutritional caloric support and complete physical rest.", "Avoid alcohol and paracetamol overdose.", "Strict hygiene."],
        "red_flags": ["Confusion, flapping tremors of hands, severe lethargy (Hepatic Encephalopathy - Emergency)", "Bruising or bleeding easily"]
    }
}

# Master List of all unique symptoms across the dataset
ALL_SYMPTOMS = sorted(list(set(
    sym
    for dis in DISEASE_DEFINITIONS.values()
    for sym in (dis["core_symptoms"] + dis["secondary_symptoms"] + dis["rare_symptoms"])
)))

# EHR History Feature List
EHR_FEATURES = [
    "age",
    "gender_male",
    "is_smoker",
    "alcohol_use",
    "has_hypertension",
    "has_diabetes",
    "has_asthma",
    "has_heart_disease",
    "has_allergies",
    "family_heart_disease",
    "family_diabetes",
    "family_allergies",
    "family_autoimmune",
    "family_gout",
    "family_migraine",
    "high_bp_reading",
    "high_glucose_reading",
    "high_cholesterol_reading",
    "bmi_high"
]

def generate_patient_cases(n_samples=6000, random_seed=42):
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    diseases = list(DISEASE_DEFINITIONS.keys())
    data = []
    
    samples_per_disease = n_samples // len(diseases)
    
    for disease_name, d_info in DISEASE_DEFINITIONS.items():
        core = d_info["core_symptoms"]
        sec = d_info["secondary_symptoms"]
        rare = d_info["rare_symptoms"]
        assoc = d_info["ehr_associations"]
        
        for _ in range(samples_per_disease):
            row = {}
            row["target_disease"] = disease_name
            
            # --- Generate Symptoms ---
            # 1. Pick core symptoms with high probability (85% - 100%)
            for sym in ALL_SYMPTOMS:
                row[sym] = 0
                
            # Present core symptoms (choose 70% to 100% of core)
            num_core = max(1, random.randint(int(len(core) * 0.7), len(core)))
            selected_core = random.sample(core, num_core)
            for s in selected_core:
                row[s] = 1
                
            # Present secondary symptoms (choose 25% to 60% of secondary)
            if sec:
                num_sec = random.randint(0, min(len(sec), max(1, int(len(sec) * 0.6))))
                selected_sec = random.sample(sec, num_sec)
                for s in selected_sec:
                    row[s] = 1
                    
            # Present rare symptoms (choose 0 to 1)
            if rare and random.random() < 0.25:
                s = random.choice(rare)
                row[s] = 1
                
            # Add occasional noise symptom (5% chance)
            if random.random() < 0.08:
                random_sym = random.choice(ALL_SYMPTOMS)
                row[random_sym] = 1
                
            # --- Generate Patient Demographics & EHR History ---
            # Base demographics
            age = random.randint(18, 85)
            gender_male = random.choice([0, 1])
            
            # Base risks
            is_smoker = 1 if random.random() < (0.35 if assoc.get("is_smoker") else 0.18) else 0
            alcohol_use = 1 if random.random() < (0.40 if assoc.get("alcohol_use") else 0.20) else 0
            
            # Age-dependent baseline risks modulated by disease associations
            has_htn = 1 if random.random() < (0.75 if assoc.get("has_hypertension") else (0.45 if age > 55 else 0.15)) else 0
            has_dm = 1 if random.random() < (0.75 if assoc.get("has_diabetes") else (0.35 if age > 50 else 0.10)) else 0
            has_asthma = 1 if random.random() < (0.85 if assoc.get("has_asthma") else 0.10) else 0
            has_cad = 1 if random.random() < (0.80 if assoc.get("has_heart_disease") else (0.30 if age > 60 else 0.05)) else 0
            has_allergy = 1 if random.random() < (0.85 if assoc.get("has_allergies") else 0.20) else 0
            
            # Family History
            fam_cad = 1 if random.random() < (0.65 if assoc.get("family_heart_disease") else 0.22) else 0
            fam_dm = 1 if random.random() < (0.70 if assoc.get("family_diabetes") else 0.25) else 0
            fam_all = 1 if random.random() < (0.70 if assoc.get("family_allergies") else 0.18) else 0
            fam_auto = 1 if random.random() < (0.65 if assoc.get("family_autoimmune") else 0.12) else 0
            fam_gout = 1 if random.random() < (0.65 if assoc.get("family_gout") else 0.10) else 0
            fam_mig = 1 if random.random() < (0.75 if assoc.get("family_migraine") else 0.15) else 0
            
            # Clinical Vitals / Lab markers
            high_bp = 1 if has_htn or random.random() < (0.80 if assoc.get("high_bp_reading") else 0.20) else 0
            high_glu = 1 if has_dm or random.random() < (0.80 if assoc.get("high_glucose_reading") else 0.18) else 0
            high_chol = 1 if has_cad or random.random() < (0.75 if assoc.get("high_cholesterol_reading") else 0.25) else 0
            bmi_high = 1 if random.random() < (0.60 if assoc.get("bmi_high") else 0.28) else 0
            
            row["age"] = age
            row["gender_male"] = gender_male
            row["is_smoker"] = is_smoker
            row["alcohol_use"] = alcohol_use
            row["has_hypertension"] = has_htn
            row["has_diabetes"] = has_dm
            row["has_asthma"] = has_asthma
            row["has_heart_disease"] = has_cad
            row["has_allergies"] = has_allergy
            row["family_heart_disease"] = fam_cad
            row["family_diabetes"] = fam_dm
            row["family_allergies"] = fam_all
            row["family_autoimmune"] = fam_auto
            row["family_gout"] = fam_gout
            row["family_migraine"] = fam_mig
            row["high_bp_reading"] = high_bp
            row["high_glucose_reading"] = high_glu
            row["high_cholesterol_reading"] = high_chol
            row["bmi_high"] = bmi_high
            
            data.append(row)
            
    df = pd.DataFrame(data)
    # Shuffle dataframe
    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return df

def main():
    os.makedirs("c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/dataset", exist_ok=True)
    os.makedirs("c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models", exist_ok=True)
    
    print("Generating comprehensive multi-modal clinical dataset...")
    df = generate_patient_cases(n_samples=6000, random_seed=42)
    
    csv_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/dataset/disease_symptoms.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} patient cases with {len(df.columns)-1} features across {len(DISEASE_DEFINITIONS)} conditions.")
    print(f"Saved dataset to {csv_path}")
    
    # Save Disease Metadata JSON
    metadata_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/dataset/disease_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(DISEASE_DEFINITIONS, f, indent=2)
    print(f"Saved disease clinical metadata to {metadata_path}")
    
    # Save Master Symptom List with Human-readable labels and tags
    symptoms_catalog = []
    for s in ALL_SYMPTOMS:
        label = s.replace("_", " ").capitalize()
        category = "General"
        if any(k in s for k in ["cough", "throat", "breath", "wheez", "sputum", "phlegm", "nose", "sinus", "sneez", "smell"]):
            category = "Respiratory & ENT"
        elif any(k in s for k in ["chest", "heart", "palpitat", "flushing"]):
            category = "Cardiovascular"
        elif any(k in s for k in ["stomach", "abdomin", "nausea", "vomit", "diarrhea", "heartburn", "bloat", "bowel", "stool", "belch", "reflux"]):
            category = "Gastrointestinal"
        elif any(k in s for k in ["headache", "dizz", "weakness", "speech", "vision", "numb", "tingl", "balance", "confus", "aura"]):
            category = "Neurological"
        elif any(k in s for k in ["skin", "rash", "itch", "plaque", "nail", "crust", "flak"]):
            category = "Dermatological"
        elif any(k in s for k in ["joint", "muscle", "back", "neck", "stiff", "toe", "crepitus"]):
            category = "Musculoskeletal"
        elif any(k in s for k in ["urin", "pelvic", "flank"]):
            category = "Urological & Renal"
        elif any(k in s for k in ["fever", "chill", "sweat", "appetite", "thirst", "weight", "fatigue"]):
            category = "Constitutional / Metabolic"
            
        symptoms_catalog.append({
            "id": s,
            "label": label,
            "category": category
        })
        
    symptoms_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/symptom_list.json"
    with open(symptoms_path, "w", encoding="utf-8") as f:
        json.dump(symptoms_catalog, f, indent=2)
    print(f"Saved {len(symptoms_catalog)} cataloged symptoms to {symptoms_path}")
    
    # Save Feature schema definition
    feature_meta = {
        "all_symptoms": ALL_SYMPTOMS,
        "ehr_features": EHR_FEATURES,
        "all_feature_columns": ALL_SYMPTOMS + EHR_FEATURES,
        "num_diseases": len(DISEASE_DEFINITIONS),
        "disease_names": sorted(list(DISEASE_DEFINITIONS.keys()))
    }
    feature_meta_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/feature_metadata.json"
    with open(feature_meta_path, "w", encoding="utf-8") as f:
        json.dump(feature_meta, f, indent=2)
    print(f"Saved feature metadata schema to {feature_meta_path}")

if __name__ == "__main__":
    main()

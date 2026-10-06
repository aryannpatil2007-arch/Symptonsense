"""
Disease Knowledge Base & Metadata for SymptomSense ML Engine
Contains clinical disease profiles, symptom correlations, urgency, ICD-10 codes,
specialist mappings, red flags, and home-care protocols.
"""

DISEASE_METADATA = {
    "Common Cold": {
        "id": "common_cold",
        "name": "Common Cold (Viral Upper Respiratory Infection)",
        "category": "Respiratory",
        "icd10": "J00",
        "urgency": "Low",
        "specialist": "General Physician / Family Practitioner",
        "description": "A mild viral infectious disease of the upper respiratory tract that primarily affects the nose, throat, and sinuses.",
        "recommended_actions": [
            "Rest adequately and drink plenty of fluids (water, herbal teas, warm broth).",
            "Use over-the-counter decongestants, saline nasal spray, or lozenges for symptom relief.",
            "Schedule a routine consultation if symptoms persist for more than 10-14 days."
        ],
        "home_care": [
            "Warm steam inhalation 2-3 times daily.",
            "Saltwater gargles for sore throat relief.",
            "Elevate head with an extra pillow during sleep to reduce nasal congestion."
        ],
        "red_flags": [
            "Difficulty breathing or persistent shortness of breath",
            "High fever above 39°C (102.2°F) lasting more than 3 days",
            "Severe chest pain or confusion"
        ],
        "typical_symptoms": ["runny_nose", "nasal_congestion", "sneezing", "sore_throat", "mild_cough", "mild_fatigue", "headache"],
        "risk_factors": []
    },
    "Influenza (Flu)": {
        "id": "influenza",
        "name": "Influenza (Acute Viral Flu)",
        "category": "Infectious / Respiratory",
        "icd10": "J10.1",
        "urgency": "Medium",
        "specialist": "General Physician / Infectious Disease Specialist",
        "description": "A contagious respiratory illness caused by influenza viruses characterized by sudden onset of high fever, intense body aches, chills, and fatigue.",
        "recommended_actions": [
            "Consult a physician within 48 hours of symptom onset for potential antiviral therapy (e.g., Oseltamivir).",
            "Isolate at home to avoid spreading infection to high-risk individuals.",
            "Monitor body temperature and hydration status closely."
        ],
        "home_care": [
            "Strict bed rest and ample oral hydration with electrolytes.",
            "Acetaminophen or Ibuprofen for fever and muscle aches (avoid aspirin in children/teens).",
            "Warm honey-lemon tea for cough soothing."
        ],
        "red_flags": [
            "Shortness of breath or rapid breathing",
            "Bluish lips or fingertips (cyanosis)",
            "Sudden dizziness, confusion, or inability to keep fluids down"
        ],
        "typical_symptoms": ["high_fever", "chills", "severe_body_aches", "fatigue", "headache", "dry_cough", "sore_throat", "sweating"],
        "risk_factors": ["age_over_65", "has_asthma", "has_diabetes"]
    },
    "COVID-19": {
        "id": "covid19",
        "name": "COVID-19 (SARS-CoV-2 Infection)",
        "category": "Infectious / Respiratory",
        "icd10": "U07.1",
        "urgency": "Medium",
        "specialist": "Pulmonologist / Infectious Disease Physician",
        "description": "A respiratory infection caused by the SARS-CoV-2 coronavirus with symptoms ranging from mild cold-like symptoms to severe hypoxemic pneumonia.",
        "recommended_actions": [
            "Perform a rapid antigen test (RAT) or RT-PCR test immediately.",
            "Self-isolate according to CDC/WHO guidelines.",
            "Check pulse oximeter oxygen saturation (SpO2) every 4–6 hours.",
            "Consult your healthcare provider if you have underlying conditions (hypertension, diabetes, asthma)."
        ],
        "home_care": [
            "Stay isolated in a well-ventilated room.",
            "Maintain hydration and track temperature and SpO2.",
            "Prone positioning (lying on stomach) to assist oxygenation if recommended."
        ],
        "red_flags": [
            "SpO2 oxygen saturation dropping below 94%",
            "Severe shortness of breath or persistent chest pressure",
            "Confusion, extreme drowsiness, or inability to wake up"
        ],
        "typical_symptoms": ["fever", "dry_cough", "loss_of_smell", "loss_of_taste", "fatigue", "shortness_of_breath", "body_aches", "sore_throat", "headache"],
        "risk_factors": ["age_over_65", "has_hypertension", "has_diabetes", "is_smoker", "bmi_high"]
    },
    "Bacterial Pneumonia": {
        "id": "pneumonia",
        "name": "Pneumonia (Lower Respiratory Infection)",
        "category": "Respiratory",
        "icd10": "J18.9",
        "urgency": "High",
        "specialist": "Pulmonologist / Internal Medicine",
        "description": "Infection that inflames air sacs in one or both lungs, which may fill with fluid or purulent material causing productive cough, fever, and hypoxemia.",
        "recommended_actions": [
            "Urgent clinical examination and Chest X-Ray / CT within 12-24 hours.",
            "Prescription antibiotics, sputum culture, and blood panel as ordered by doctor.",
            "Seek hospital admission if SpO2 is compromised or respiratory distress occurs."
        ],
        "home_care": [
            "Complete the entire course of prescribed antibiotics without stopping early.",
            "Drink warm fluids to loosen mucus in lungs.",
            "Use a cool-mist humidifier."
        ],
        "red_flags": [
            "Severe difficulty breathing or rapid gasping",
            "Coughing up rust-colored or bloody sputum",
            "Cyanosis (blue tint on lips or nails), high fever with delirium"
        ],
        "typical_symptoms": ["high_fever", "chills", "shortness_of_breath", "productive_cough", "phlegm_production", "chest_pain_on_breathing", "fatigue", "sweating"],
        "risk_factors": ["age_over_65", "is_smoker", "has_asthma", "has_diabetes"]
    },
    "Bronchial Asthma Flare-up": {
        "id": "asthma",
        "name": "Bronchial Asthma (Acute Exacerbation)",
        "category": "Respiratory / Allergic",
        "icd10": "J45.9",
        "urgency": "High",
        "specialist": "Pulmonologist / Allergist",
        "description": "A chronic condition in which airways narrow, swell, and produce extra mucus, causing wheezing, breathlessness, and chest tightness.",
        "recommended_actions": [
            "Use prescribed fast-acting rescue inhaler (e.g., Albuterol/Salbutamol) immediately (2-4 puffs).",
            "Follow personal Asthma Action Plan.",
            "If symptoms do not improve within 15-20 minutes, seek emergency department care immediately."
        ],
        "home_care": [
            "Sit upright; do not lie down flat.",
            "Remove exposure to allergens, dust, smoke, or cold air.",
            "Practice slow, pursed-lip breathing."
        ],
        "red_flags": [
            "Struggling to speak full sentences in one breath",
            "Inhaler provides no relief or symptoms worsen rapidly",
            "Retractions (chest and neck skin sucking inward during breathing)"
        ],
        "typical_symptoms": ["wheezing", "shortness_of_breath", "chest_tightness", "dry_cough", "difficulty_breathing_at_night"],
        "risk_factors": ["has_asthma", "has_allergies", "is_smoker", "family_allergies"]
    },
    "Hypertension (High Blood Pressure Crisis/Stage)": {
        "id": "hypertension",
        "name": "Hypertension (Elevated Blood Pressure)",
        "category": "Cardiovascular",
        "icd10": "I10",
        "urgency": "High",
        "specialist": "Cardiologist / General Physician",
        "description": "Persistently elevated systemic arterial blood pressure that strains cardiac and vascular systems.",
        "recommended_actions": [
            "Measure BP after 5 minutes of quiet sitting using an accurate cuff.",
            "If BP is >= 180/120 mmHg without other symptoms, recheck in 5 min. If still elevated, seek urgent medical evaluation.",
            "Consult a cardiologist to optimize antihypertensive medication regimens."
        ],
        "home_care": [
            "Adopt the DASH diet (low sodium, rich in potassium, leafy greens, fiber).",
            "Engage in moderate daily aerobic exercise (30 mins).",
            "Eliminate tobacco and limit alcohol intake; manage chronic stress."
        ],
        "red_flags": [
            "Severe sudden headache with visual disturbance",
            "Chest pain, numbness, slurred speech, or weakness on one side of body (Seek 911 / ER immediately)"
        ],
        "typical_symptoms": ["headache_morning", "dizziness", "palpitations", "vision_blur", "nosebleed", "fatigue"],
        "risk_factors": ["has_hypertension", "high_bp_reading", "age_over_45", "is_smoker", "bmi_high", "family_heart_disease"]
    },
    "Coronary Artery Disease / Angina": {
        "id": "cad_angina",
        "name": "Coronary Artery Disease / Angina Pectoris",
        "category": "Cardiovascular",
        "icd10": "I25.10",
        "urgency": "Emergency",
        "specialist": "Cardiologist / Emergency Physician",
        "description": "Reduced blood flow to the heart muscle due to plaque accumulation in coronary arteries, causing cardiac ischemia and chest pressure.",
        "recommended_actions": [
            "If experiencing active crushing chest pressure radiating to arm, jaw, neck, or back: CALL EMERGENCY SERVICES (911/112) IMMEDIATELY.",
            "Chew one adult aspirin (325 mg) unless contraindicated by known allergy.",
            "Rest completely in a comfortable semi-recumbent position."
        ],
        "home_care": [
            "Cardiac rehabilitation under medical supervision once stabilized.",
            "Strict lipid management, blood pressure control, and antiplatelet therapy as prescribed.",
            "Avoid strenuous exertion until cleared by cardiologist."
        ],
        "red_flags": [
            "Crushing substernal chest pressure lasting > 5 minutes",
            "Pain radiating to left arm, neck, jaw, or shoulder blade",
            "Diaphoresis (cold sweats), severe shortness of breath, impending sense of doom"
        ],
        "typical_symptoms": ["chest_pain", "chest_pressure_radiating", "shortness_of_breath", "cold_sweating", "nausea", "dizziness", "palpitations"],
        "risk_factors": ["has_heart_disease", "has_hypertension", "has_diabetes", "high_cholesterol_reading", "is_smoker", "age_over_45", "family_heart_disease"]
    },
    "Type 2 Diabetes (Hyperglycemia / Metabolic Dysregulation)": {
        "id": "diabetes_t2",
        "name": "Type 2 Diabetes Mellitus",
        "category": "Metabolic & Endocrine",
        "icd10": "E11.9",
        "urgency": "Medium",
        "specialist": "Endocrinologist / Diabetologist",
        "description": "A chronic metabolic disorder characterized by insulin resistance and relative insulin deficiency resulting in persistent hyperglycemia.",
        "recommended_actions": [
            "Perform fasting blood glucose and HbA1c blood test.",
            "Consult an endocrinologist for personalized glycemic targets and medication plan (e.g. Metformin, SGLT2i, GLP-1 RA).",
            "Schedule regular diabetic foot and dilated eye examinations."
        ],
        "home_care": [
            "Monitor fingerstick or continuous glucose levels regularly.",
            "Follow a balanced low-glycemic Mediterranean or carbohydrate-controlled diet.",
            "Maintain daily foot care and stay physically active."
        ],
        "red_flags": [
            "Fruity breath odor, deep rapid breathing, confusion (Diabetic Ketoacidosis risk)",
            "Blood glucose level > 300 mg/dL accompanied by nausea or vomiting",
            "Non-healing ulcers or infections on lower extremities"
        ],
        "typical_symptoms": ["excessive_thirst", "frequent_urination", "excessive_hunger", "unexplained_weight_loss", "fatigue", "vision_blur", "slow_healing_wounds", "tingling_hands_feet"],
        "risk_factors": ["has_diabetes", "family_diabetes", "high_glucose_reading", "bmi_high", "age_over_45"]
    },
    "Gastroesophageal Reflux Disease (GERD)": {
        "id": "gerd",
        "name": "GERD (Acid Reflux)",
        "category": "Gastrointestinal",
        "icd10": "K21.9",
        "urgency": "Low",
        "specialist": "Gastroenterologist / General Physician",
        "description": "A digestive disorder in which stomach acid repeatedly flows back into the tube connecting mouth and stomach, causing heartburn and mucosal irritation.",
        "recommended_actions": [
            "Consult a physician for evaluation; consider a course of H2 blockers or PPIs if symptoms are frequent.",
            "Keep a food trigger diary (coffee, spicy foods, citrus, fatty meals, chocolate).",
            "Undergo upper endoscopy if symptoms fail to respond or alarm features are present."
        ],
        "home_care": [
            "Avoid lying down for at least 3 hours after eating.",
            "Elevate the head of your bed by 6 inches (15 cm).",
            "Eat smaller, more frequent meals instead of heavy dinners."
        ],
        "red_flags": [
            "Difficulty or pain while swallowing food (dysphagia)",
            "Vomiting blood or coffee-ground material, or dark tarry stools",
            "Unexplained weight loss or severe chest pain not relieved by antacids"
        ],
        "typical_symptoms": ["heartburn", "acid_regurgitation", "upper_abdominal_pain", "chest_burning", "sour_taste_in_mouth", "bloating", "chronic_throat_clearing"],
        "risk_factors": ["bmi_high", "is_smoker", "alcohol_use"]
    },
    "Acute Gastroenteritis (Stomach Flu)": {
        "id": "gastroenteritis",
        "name": "Acute Gastroenteritis (Infectious Diarrhea)",
        "category": "Gastrointestinal / Infectious",
        "icd10": "A09",
        "urgency": "Medium",
        "specialist": "General Physician / Gastroenterologist",
        "description": "Inflammation of the stomach and intestines typically caused by viral or bacterial pathogens, leading to sudden vomiting and watery diarrhea.",
        "recommended_actions": [
            "Focus on aggressive oral rehydration with Oral Rehydration Salts (ORS) or electrolyte solutions.",
            "Consult a doctor if unable to keep liquids down for > 24 hours or if high fever develops.",
            "Stool culture test if blood is present in stool."
        ],
        "home_care": [
            "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) once vomiting subsides.",
            "Avoid dairy, caffeine, alcohol, fatty foods, and spicy seasonings.",
            "Wash hands thoroughly with soap and water to prevent household transmission."
        ],
        "red_flags": [
            "Signs of severe dehydration (dry mouth, sunken eyes, no urine for > 8 hours, severe dizziness on standing)",
            "High fever above 38.8°C (102°F) or bloody stools (dysentery)",
            "Severe unrelenting abdominal cramping"
        ],
        "typical_symptoms": ["watery_diarrhea", "nausea", "vomiting", "abdominal_cramping", "mild_fever", "loss_of_appetite", "fatigue"],
        "risk_factors": []
    },
    "Peptic Ulcer Disease": {
        "id": "peptic_ulcer",
        "name": "Peptic Ulcer Disease (Gastric / Duodenal Ulcer)",
        "category": "Gastrointestinal",
        "icd10": "K27.9",
        "urgency": "Medium",
        "specialist": "Gastroenterologist",
        "description": "Sores that develop on the inside lining of the stomach and upper portion of small intestine, often due to H. pylori infection or long-term NSAID use.",
        "recommended_actions": [
            "Consult a gastroenterologist for H. pylori testing (breath test, stool antigen, or endoscopy).",
            "Prescribed acid suppression (PPIs) and antibiotic eradication therapy if positive for H. pylori.",
            "Discontinue NSAID pain relievers (ibuprofen, naproxen, aspirin) unless instructed by cardiologist."
        ],
        "home_care": [
            "Eat regular meals; avoid skipping meals.",
            "Avoid alcohol and smoking which delay mucosal healing.",
            "Avoid acidic, spicy, or irritating foods."
        ],
        "red_flags": [
            "Black, tarry, foul-smelling stools (melena)",
            "Vomiting red blood or granular black material (hematemesis)",
            "Sudden, excruciating, rigid abdominal pain (possible perforation - CALL ER!)"
        ],
        "typical_symptoms": ["burning_stomach_pain", "feeling_of_fullness", "bloating", "belching", "nausea", "heartburn", "pain_worse_between_meals"],
        "risk_factors": ["is_smoker", "alcohol_use", "age_over_45"]
    },
    "Acute Appendicitis": {
        "id": "appendicitis",
        "name": "Acute Appendicitis",
        "category": "Gastrointestinal / Surgical Emergency",
        "icd10": "K35.80",
        "urgency": "Emergency",
        "specialist": "General Surgeon / Emergency Department",
        "description": "Acute inflammation of the vermiform appendix, requiring urgent surgical appendectomy to prevent perforation and peritonitis.",
        "recommended_actions": [
            "GO TO THE NEAREST EMERGENCY ROOM IMMEDIATELY.",
            "Do NOT eat, drink, or take laxatives/heating pads as these can trigger rupture.",
            "Emergency ultrasound or abdominal CT scan will be performed."
        ],
        "home_care": [
            "NO home treatment is safe. Immediate surgical evaluation is mandatory."
        ],
        "red_flags": [
            "Sharp pain starting around navel and migrating to the lower right abdomen (McBurney's point)",
            "Rebound tenderness (worse when letting go of pressed abdomen)",
            "Fever with vomiting and inability to pass gas"
        ],
        "typical_symptoms": ["lower_right_abdominal_pain", "nausea", "vomiting", "loss_of_appetite", "low_grade_fever", "abdominal_swelling_tenderness"],
        "risk_factors": []
    },
    "Acute Migraine Attack": {
        "id": "migraine",
        "name": "Migraine Headache (with or without Aura)",
        "category": "Neurological",
        "icd10": "G43.909",
        "urgency": "Medium",
        "specialist": "Neurologist / Headache Specialist",
        "description": "A primary neurological headache disorder characterized by recurrent moderate-to-severe throbbing attacks, often unilateral, with sensory sensitivities.",
        "recommended_actions": [
            "Take prescribed acute migraine medication (Triptans, Gepants, or NSAIDs) at the earliest sign of attack.",
            "Maintain a migraine diary to identify dietary, sleep, stress, or hormonal triggers.",
            "Consult a neurologist for preventive therapy if attacks occur > 3-4 days per month."
        ],
        "home_care": [
            "Rest in a completely dark, quiet room with cool compress on forehead/neck.",
            "Drink plenty of water and practice deep calming relaxation techniques.",
            "Avoid bright screens and sudden loud noises."
        ],
        "red_flags": [
            "Thunderclap headache: explosive maximum intensity within 60 seconds (requires immediate brain scan)",
            "Headache accompanied by fever, neck stiffness, confusion, or weakness on one side",
            "New onset severe headache after age 50"
        ],
        "typical_symptoms": ["throbbing_headache", "unilateral_head_pain", "sensitivity_to_light", "sensitivity_to_sound", "nausea", "visual_aura", "dizziness"],
        "risk_factors": ["has_allergies", "family_migraine"]
    },
    "Ischemic Stroke / Transient Ischemic Attack (TIA)": {
        "id": "stroke_tia",
        "name": "Acute Stroke / TIA (Cerebrovascular Event)",
        "category": "Neurological / Emergency",
        "icd10": "I63.9",
        "urgency": "Emergency",
        "specialist": "Stroke Neurologist / Emergency Physician",
        "description": "Sudden interruption of blood supply to the brain caused by a clot (thrombus or embolus), causing rapid death of neural tissue.",
        "recommended_actions": [
            "ACT FAST: CALL 911 / 112 IMMEDIATELY. Time is brain tissue! Thrombolytic therapy (tPA) is most effective within 3-4.5 hours of onset.",
            "Note the exact minute symptoms began.",
            "Do NOT give the person food, water, or aspirin until evaluated at hospital."
        ],
        "home_care": [
            "NO home treatment. Keep patient lying flat on side if vomiting, and await EMS."
        ],
        "red_flags": [
            "Face drooping on one side (ask them to smile)",
            "Arm weakness or drift (ask them to raise both arms)",
            "Speech difficulty (slurred words or inability to understand/speak)",
            "Sudden loss of balance, vision loss in one eye, or severe vertigo"
        ],
        "typical_symptoms": ["facial_weakness", "arm_leg_weakness", "slurred_speech", "sudden_confusion", "vision_loss_one_eye", "sudden_severe_dizziness", "loss_of_balance"],
        "risk_factors": ["has_hypertension", "has_diabetes", "has_heart_disease", "is_smoker", "high_cholesterol_reading", "age_over_65"]
    },
    "Urinary Tract Infection (UTI / Cystitis)": {
        "id": "uti",
        "name": "Urinary Tract Infection (Acute Cystitis)",
        "category": "Infectious / Urological",
        "icd10": "N39.0",
        "urgency": "Medium",
        "specialist": "Urologist / General Physician",
        "description": "An infection in any part of the urinary system (kidneys, bladder, ureters, urethra), most commonly bacterial bladder inflammation.",
        "recommended_actions": [
            "Obtain a urine routine and microscopic culture test (clean-catch midstream sample).",
            "Consult doctor for targeted antibiotic treatment (e.g. Nitrofurantoin, Fosfomycin, Trimethoprim).",
            "Finish the entire antibiotic course."
        ],
        "home_care": [
            "Drink plenty of water (2.5 to 3 liters daily) to flush urinary tract.",
            "Urinate whenever the urge arises; do not hold urine.",
            "Apply a warm heating pad to lower abdomen to soothe pelvic discomfort."
        ],
        "red_flags": [
            "High fever with flank (back/side) pain and shaking chills (indicates Pyelonephritis/Kidney infection)",
            "Severe hematuria (visible blood/clots in urine)",
            "Inability to pass urine"
        ],
        "typical_symptoms": ["burning_urination", "frequent_urination", "urgency_to_urinate", "cloudy_foul_urine", "pelvic_pain", "blood_in_urine"],
        "risk_factors": ["has_diabetes"]
    },
    "Allergic Rhinitis / Hay Fever": {
        "id": "allergic_rhinitis",
        "name": "Allergic Rhinitis (Seasonal / Perennial Allergies)",
        "category": "Allergic / Immunology",
        "icd10": "J30.9",
        "urgency": "Low",
        "specialist": "Allergist / ENT Specialist",
        "description": "An allergic response causing itchy, watery eyes, sneezing, and other symptoms triggered by airborne allergens (pollen, dust mites, pet dander).",
        "recommended_actions": [
            "Use non-drowsy oral antihistamines (Cetirizine, Loratadine, Fexofenadine) or corticosteroid nasal sprays.",
            "Consider allergen immunotherapy (allergy shots or sublingual tablets) for long-term tolerance.",
            "Track pollen counts and avoid peak outdoors exposure."
        ],
        "home_care": [
            "Saline nasal irrigation (Neti pot with distilled/sterile water).",
            "Keep windows closed during high pollen seasons and run HEPA air purifier.",
            "Wash bedding weekly in hot water (60°C/140°F) to eliminate dust mites."
        ],
        "red_flags": [
            "Swelling of tongue, lips, or throat (Anaphylaxis risk - USE EPIPEN AND CALL 911)",
            "Severe difficulty breathing or wheezing"
        ],
        "typical_symptoms": ["sneezing", "itchy_eyes", "watery_eyes", "runny_nose", "nasal_congestion", "itchy_throat", "post_nasal_drip"],
        "risk_factors": ["has_allergies", "has_asthma", "family_allergies"]
    },
    "Eczema (Atopic Dermatitis)": {
        "id": "eczema",
        "name": "Atopic Dermatitis (Eczema)",
        "category": "Dermatological",
        "icd10": "L20.9",
        "urgency": "Low",
        "specialist": "Dermatologist",
        "description": "A chronic inflammatory skin condition characterized by dry, red, itchy, and irritated patches, commonly in the skin flexures.",
        "recommended_actions": [
            "Consult a dermatologist for topical corticosteroid or calcineurin inhibitor prescription during flares.",
            "Identify and eliminate contact irritants (harsh soaps, fragrance, wool fabrics).",
            "Patch testing if contact allergy is suspected."
        ],
        "home_care": [
            "Apply thick ceramide-rich moisturizing creams immediately after lukewarm bathing (3-minute rule).",
            "Take short lukewarm showers instead of hot baths.",
            "Keep fingernails trimmed to minimize scratch damage and secondary bacterial infection."
        ],
        "red_flags": [
            "Crusting with golden-yellow oozing fluid (bacterial Impetigo superinfection)",
            "Widespread rapid rash spread with fever (Eczema herpeticum)"
        ],
        "typical_symptoms": ["intense_skin_itching", "red_dry_skin_patches", "skin_flaking", "cracked_skin", "skin_lichenification"],
        "risk_factors": ["has_allergies", "has_asthma", "family_allergies"]
    },
    "Psoriasis": {
        "id": "psoriasis",
        "name": "Psoriasis Vulgaris",
        "category": "Dermatological / Autoimmune",
        "icd10": "L40.0",
        "urgency": "Low",
        "specialist": "Dermatologist / Rheumatologist",
        "description": "An immune-mediated chronic skin disease that causes rapid buildup of skin cells, leading to silvery scaled plaques on elbows, knees, and scalp.",
        "recommended_actions": [
            "Consult a dermatologist for topical vitamin D analogues, retinoids, phototherapy, or biologic therapy.",
            "Screen for associated Psoriatic Arthritis (joint pain/stiffness).",
            "Maintain cardiovascular risk screening due to systemic inflammation."
        ],
        "home_care": [
            "Keep skin lubricated with heavy emollients.",
            "Moderate brief sunlight exposure (10-15 minutes).",
            "Avoid skin injury, cuts, and scrapes (Koebner phenomenon)."
        ],
        "red_flags": [
            "Sudden red peeling rash covering entire body with fever (Erythrodermic psoriasis - ER emergency)",
            "Severe swelling and pain in finger and toe joints"
        ],
        "typical_symptoms": ["silvery_scaled_skin_plaques", "red_thickened_skin_patches", "dry_cracked_skin", "itching_skin_plaques", "pitted_nails", "joint_stiffness"],
        "risk_factors": ["family_autoimmune", "is_smoker", "bmi_high"]
    },
    "Hypothyroidism": {
        "id": "hypothyroidism",
        "name": "Hypothyroidism (Underactive Thyroid)",
        "category": "Metabolic & Endocrine",
        "icd10": "E03.9",
        "urgency": "Medium",
        "specialist": "Endocrinologist",
        "description": "A condition where the thyroid gland does not produce enough thyroid hormones, slowing down the body's metabolic processes.",
        "recommended_actions": [
            "Test serum Thyroid-Stimulating Hormone (TSH) and Free T4 levels.",
            "Prescription thyroid hormone replacement (Levothyroxine) taken consistently on empty stomach.",
            "Follow-up TSH blood test every 6-8 weeks until optimal dosage is reached."
        ],
        "home_care": [
            "Take levothyroxine with a full glass of water 30-60 minutes before breakfast.",
            "Avoid taking calcium, iron, or antacids within 4 hours of thyroid medication.",
            "Maintain a fiber-rich balanced diet to prevent constipation."
        ],
        "red_flags": [
            "Extreme lethargy, hypothermia, slow heart rate, severe swelling, confusion (Myxedema coma - Medical Emergency)"
        ],
        "typical_symptoms": ["unexplained_weight_gain", "severe_fatigue", "cold_intolerance", "constipation", "dry_skin", "hair_thinning", "depressed_mood", "muscle_weakness"],
        "risk_factors": ["family_autoimmune", "age_over_45"]
    },
    "Hyperthyroidism": {
        "id": "hyperthyroidism",
        "name": "Hyperthyroidism (Overactive Thyroid / Graves')",
        "category": "Metabolic & Endocrine",
        "icd10": "E05.90",
        "urgency": "Medium",
        "specialist": "Endocrinologist",
        "description": "Overproduction of thyroid hormone causing an accelerated metabolic state, weight loss, tachycardia, and heat intolerance.",
        "recommended_actions": [
            "Blood panel for TSH, Free T3, Free T4, and TSH receptor antibodies (TRAb).",
            "Cardiology evaluation for beta-blockers to control rapid heart rate.",
            "Consult endocrinologist for antithyroid drugs (Methimazole/PTU) or radioactive iodine."
        ],
        "home_care": [
            "Ensure adequate caloric intake with nutritious whole foods.",
            "Avoid excessive iodine supplements or kelp/seaweed.",
            "Practice stress-reduction techniques."
        ],
        "red_flags": [
            "Thyroid storm: high fever, extreme agitation, delirium, pulse > 140 bpm, vomiting (Emergency!)"
        ],
        "typical_symptoms": ["unexplained_weight_loss", "rapid_heartbeat", "palpitations", "heat_intolerance", "nervousness_anxiety", "hand_tremors", "excessive_sweating", "bulging_eyes"],
        "risk_factors": ["family_autoimmune"]
    },
    "Osteoarthritis": {
        "id": "osteoarthritis",
        "name": "Osteoarthritis (Degenerative Joint Disease)",
        "category": "Musculoskeletal",
        "icd10": "M19.90",
        "urgency": "Low",
        "specialist": "Orthopedic Specialist / Rheumatologist",
        "description": "The most common form of arthritis, occurring when the protective cartilage that cushions the ends of bones wears down over time.",
        "recommended_actions": [
            "Consult an orthopedic doctor or physical therapist for tailored joint-strengthening regimens.",
            "X-ray imaging of affected joints (knees, hips, spine, hands).",
            "Consider topical NSAIDs, oral analgesics, or intra-articular hyaluronic acid/corticosteroid injections."
        ],
        "home_care": [
            "Engage in low-impact exercises (swimming, stationary cycling, walking).",
            "Apply warm compresses before exercise for stiffness, and cold packs after for inflammation.",
            "Weight management to relieve compressive force on weight-bearing joints."
        ],
        "red_flags": [
            "Joint becomes suddenly hot, severely red, swollen, and accompanied by fever (Septic arthritis - Emergency)"
        ],
        "typical_symptoms": ["joint_pain_worse_with_activity", "joint_stiffness_morning_brief", "crepitus_grating_sound", "loss_of_joint_flexibility", "bone_spurs_swelling"],
        "risk_factors": ["age_over_45", "bmi_high"]
    },
    "Rheumatoid Arthritis": {
        "id": "rheumatoid_arthritis",
        "name": "Rheumatoid Arthritis (Autoimmune Inflammatory Arthritis)",
        "category": "Musculoskeletal / Autoimmune",
        "icd10": "M06.9",
        "urgency": "Medium",
        "specialist": "Rheumatologist",
        "description": "A chronic systemic autoimmune disorder causing symmetric inflammatory polyarthritis, synovitis, joint destruction, and extra-articular manifestations.",
        "recommended_actions": [
            "Urgent rheumatology consultation for early initiation of DMARDs (e.g., Methotrexate, Biologics) to prevent permanent joint erosion.",
            "Blood panel: Rheumatoid Factor (RF), Anti-CCP antibodies, ESR, and CRP.",
            "Baseline joint radiographs and ultrasound."
        ],
        "home_care": [
            "Balance gentle exercise with rest during acute flare-ups.",
            "Use assistive joint-friendly devices for opening jars and daily tasks.",
            "Anti-inflammatory Mediterranean diet."
        ],
        "red_flags": [
            "Severe cervical spine pain or neurological symptoms in arms/legs",
            "High fever with acute single-joint hot swelling"
        ],
        "typical_symptoms": ["symmetric_joint_pain", "morning_joint_stiffness_prolonged", "swollen_warm_joints", "hand_finger_joint_swelling", "chronic_fatigue", "low_grade_fever"],
        "risk_factors": ["family_autoimmune", "is_smoker"]
    },
    "Acute Sinusitis": {
        "id": "sinusitis",
        "name": "Acute Rhinosinusitis (Sinus Infection)",
        "category": "Respiratory / ENT",
        "icd10": "J01.90",
        "urgency": "Low",
        "specialist": "ENT Specialist / General Physician",
        "description": "Inflammation and congestion of the tissue lining the paranasal sinuses, causing facial pressure, thick nasal drainage, and headache.",
        "recommended_actions": [
            "Most cases are viral and resolve within 7-10 days with symptomatic management.",
            "If symptoms last > 10 days or worsen after initial improvement ('double sickening'), consult a doctor for possible bacterial etiology and antibiotic therapy."
        ],
        "home_care": [
            "Saline nasal irrigation twice daily.",
            "Apply warm moist compresses around eyes, cheeks, and nose.",
            "Stay well hydrated to thin mucus secretions."
        ],
        "red_flags": [
            "Swelling or redness around the eyes (periorbital cellulitis)",
            "Severe unrelenting frontal headache, vision changes, or stiff neck"
        ],
        "typical_symptoms": ["facial_pain_pressure", "nasal_congestion", "thick_yellow_green_mucus", "headache_worse_bending_forward", "toothache_upper_jaw", "reduced_smell", "fatigue"],
        "risk_factors": ["has_allergies", "is_smoker"]
    },
    "Gouty Arthritis (Acute Gout Flare)": {
        "id": "gout",
        "name": "Acute Gout Flare (Uric Acid Crystal Arthritis)",
        "category": "Metabolic & Musculoskeletal",
        "icd10": "M10.9",
        "urgency": "Medium",
        "specialist": "Rheumatologist / General Physician",
        "description": "An extremely painful form of inflammatory arthritis caused by monosodium urate crystal deposition in joints due to hyperuricemia, classic at the big toe base (Podagra).",
        "recommended_actions": [
            "Initiate acute anti-inflammatory therapy (Colchicine, NSAIDs, or systemic corticosteroids) promptly.",
            "Test serum uric acid levels 2-4 weeks after the acute flare resolves.",
            "Discuss long-term urate-lowering therapy (Allopurinol, Febuxostat) if flares are recurrent."
        ],
        "home_care": [
            "Rest and elevate the affected joint; avoid bearing weight.",
            "Apply ice packs wrapped in a cloth for 20 minutes at a time.",
            "Stay heavily hydrated (drink 3+ liters water daily) to assist uric acid excretion; avoid high-purine foods (red meat, shellfish, beer, high-fructose corn syrup)."
        ],
        "red_flags": [
            "Fever and chills accompanying joint redness (rule out septic arthritis with urgent synovial fluid aspiration)"
        ],
        "typical_symptoms": ["severe_big_toe_joint_pain", "sudden_nighttime_joint_pain", "joint_swelling_intense_redness", "joint_exquisitely_tender_to_touch", "warmth_over_joint"],
        "risk_factors": ["alcohol_use", "bmi_high", "has_hypertension", "family_gout"]
    },
    "Dengue Viral Fever": {
        "id": "dengue",
        "name": "Dengue Fever (Breakbone Fever)",
        "category": "Infectious Disease",
        "icd10": "A90",
        "urgency": "High",
        "specialist": "Infectious Disease / Internal Medicine",
        "description": "A mosquito-borne viral infection causing severe flu-like illness, intense retro-orbital headache, debilitating muscle/joint pain, and potential thrombocytopenia.",
        "recommended_actions": [
            "Perform Dengue NS1 antigen test and Complete Blood Count (CBC) to monitor platelet count and hematocrit daily.",
            "Avoid NSAIDs, Aspirin, or Ibuprofen as they significantly increase bleeding risk; use Paracetamol only.",
            "Hospitalization if platelet count plummets or warning signs emerge."
        ],
        "home_care": [
            "Strict bed rest and continuous oral electrolyte replenishment (coconut water, ORS, soups).",
            "Use mosquito netting and repellents to prevent transmission to mosquitoes."
        ],
        "red_flags": [
            "Severe abdominal pain or persistent vomiting",
            "Bleeding gums, nosebleeds, or dark bruising (purpura)",
            "Lethargy, restlessness, cold clammy extremities, or hematemesis (Severe Dengue Shock)"
        ],
        "typical_symptoms": ["high_fever", "severe_pain_behind_eyes", "severe_joint_muscle_aches", "skin_rash", "nausea_vomiting", "fatigue", "mild_gum_bleeding"],
        "risk_factors": []
    }
}

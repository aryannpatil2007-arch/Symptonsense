import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models.user import User
from .models.profile import HealthProfile
from .models.record import HealthRecord
from .models.prediction import SymptomPrediction
from .services.auth_service import get_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if users already exist
        if db.query(User).count() > 0:
            print("Database already contains records. Skipping seed.")
            return

        print("Seeding demo clinical profiles and electronic health records...")
        
        # ----------------------------------------------------
        # 1. DEMO USER 1: John Doe (Cardiometabolic profile)
        # ----------------------------------------------------
        pw_hash = get_password_hash("Password123!")
        john = User(
            email="john.doe@example.com",
            full_name="John Doe",
            hashed_password=pw_hash,
            consent_given=True,
            consent_timestamp=datetime.utcnow() - timedelta(days=90)
        )
        db.add(john)
        db.flush()
        
        john_profile = HealthProfile(
            user_id=john.id,
            age=58,
            gender="male",
            blood_group="O+",
            height_cm=176.0,
            weight_kg=91.0,
            bmi=29.38,
            smoking_status="former",
            alcohol_use="occasional",
            physical_activity="sedentary",
            allergies=json.dumps(["Sulfa drugs", "Ibuprofen / NSAIDs"]),
            chronic_conditions=json.dumps(["Hypertension", "Type 2 Diabetes Mellitus", "Hyperlipidemia"]),
            current_medications=json.dumps([
                {"name": "Metformin", "dose": "500mg", "frequency": "Twice daily with meals", "purpose": "Blood Sugar Control"},
                {"name": "Amlodipine", "dose": "5mg", "frequency": "Once daily (Morning)", "purpose": "Blood Pressure"},
                {"name": "Atorvastatin", "dose": "20mg", "frequency": "Once daily (Bedtime)", "purpose": "Cholesterol Management"}
            ]),
            past_diagnoses=json.dumps(["COVID-19 (Mild) - Nov 2022", "Knee Arthroscopy - 2017"]),
            family_history=json.dumps(["heart_disease", "diabetes", "hypertension"]),
            emergency_contact_name="Sarah Doe",
            emergency_contact_phone="+1-555-019-4821",
            emergency_contact_relation="Spouse"
        )
        db.add(john_profile)
        
        # John's Historical Lab Records
        john_records = [
            HealthRecord(
                user_id=john.id,
                record_type="lab_result",
                title="Comprehensive Metabolic Panel & Lipid Profile",
                event_date=datetime.utcnow() - timedelta(days=60),
                doctor_name="Dr. Marcus Vance, MD",
                facility="St. Jude Medical Center",
                notes="Patient fasting for 12 hours. Glycemic control sub-optimal.",
                systolic_bp=148,
                diastolic_bp=92,
                heart_rate=78,
                blood_sugar_fasting=145.0,
                total_cholesterol=220.0,
                ldl_cholesterol=138.0,
                hdl_cholesterol=42.0,
                hemoglobin=14.8,
                spo2=98.0
            ),
            HealthRecord(
                user_id=john.id,
                record_type="vital_sign",
                title="Routine Cardiology Vitals Follow-up",
                event_date=datetime.utcnow() - timedelta(days=30),
                doctor_name="Dr. Marcus Vance, MD",
                facility="Heart & Vascular Clinic",
                notes="Adjusted Amlodipine dosage. Advised 30 min daily walking.",
                systolic_bp=138,
                diastolic_bp=86,
                heart_rate=74,
                blood_sugar_fasting=132.0,
                total_cholesterol=198.0,
                ldl_cholesterol=118.0,
                hdl_cholesterol=46.0,
                spo2=99.0
            ),
            HealthRecord(
                user_id=john.id,
                record_type="doctor_visit",
                title="Quarterly Diabetic Review & HbA1c",
                event_date=datetime.utcnow() - timedelta(days=10),
                doctor_name="Dr. Elena Rostova, MD (Endocrinology)",
                facility="City Health Endocrinology Center",
                notes="HbA1c measured at 7.2%. Foot inspection normal.",
                systolic_bp=134,
                diastolic_bp=84,
                heart_rate=72,
                blood_sugar_fasting=122.0,
                blood_sugar_postprandial=168.0,
                total_cholesterol=190.0,
                hemoglobin=15.1,
                spo2=98.0
            )
        ]
        db.add_all(john_records)
        
        # John's past prediction
        john_prediction = SymptomPrediction(
            user_id=john.id,
            symptoms_selected=json.dumps(["headache_morning", "dizziness", "palpitations"]),
            symptom_description="Woke up with throbbing pressure behind eyes and slight lightheadedness.",
            severity=6,
            duration="1 day",
            onset="sudden",
            is_emergency=False,
            top_condition="Hypertension Crisis",
            top_condition_icd10="I10",
            top_confidence=94.2,
            urgency="High",
            specialist="Cardiologist / General Physician",
            all_predictions=json.dumps([
                {"rank": 1, "condition": "Hypertension Crisis", "confidence": 94.2, "urgency": "High", "specialist": "Cardiologist", "icd10": "I10"},
                {"rank": 2, "condition": "Coronary Artery Disease / Angina", "confidence": 3.8, "urgency": "Emergency", "specialist": "Cardiologist", "icd10": "I25.10"},
                {"rank": 3, "condition": "Acute Migraine Attack", "confidence": 1.2, "urgency": "Medium", "specialist": "Neurologist", "icd10": "G43.909"}
            ]),
            explainability=json.dumps([
                {"feature": "headache_morning", "feature_label": "Headache morning", "impact": "positive", "contribution": 35.0, "type": "symptom"},
                {"feature": "has_hypertension", "feature_label": "History of hypertension", "impact": "positive", "contribution": 42.0, "type": "ehr_history"},
                {"feature": "high_bp_reading", "feature_label": "High bp reading", "impact": "positive", "contribution": 36.0, "type": "vital_sign"},
                {"feature": "dizziness", "feature_label": "Dizziness", "impact": "positive", "contribution": 20.0, "type": "symptom"}
            ]),
            recommended_actions=json.dumps([
                "Measure BP after 5 minutes of quiet sitting using an accurate cuff.",
                "If BP is >= 180/120 mmHg, seek urgent medical evaluation.",
                "Consult cardiologist to optimize antihypertensive medication regimens."
            ]),
            home_care=json.dumps(["Low sodium diet.", "Rest in quiet room.", "Avoid caffeine."]),
            red_flags=json.dumps(["Severe chest pain radiating to arm", "Sudden numbness or slurred speech"]),
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        db.add(john_prediction)

        # ----------------------------------------------------
        # 2. DEMO USER 2: Jane Smith (Allergy / Respiratory profile)
        # ----------------------------------------------------
        jane = User(
            email="jane.smith@example.com",
            full_name="Jane Smith",
            hashed_password=pw_hash,
            consent_given=True,
            consent_timestamp=datetime.utcnow() - timedelta(days=120)
        )
        db.add(jane)
        db.flush()
        
        jane_profile = HealthProfile(
            user_id=jane.id,
            age=28,
            gender="female",
            blood_group="A+",
            height_cm=165.0,
            weight_kg=58.0,
            bmi=21.3,
            smoking_status="never",
            alcohol_use="never",
            physical_activity="active",
            allergies=json.dumps(["Penicillin", "Pollen / Ragweed", "Peanuts", "Dust Mites"]),
            chronic_conditions=json.dumps(["Bronchial Asthma", "Allergic Rhinitis"]),
            current_medications=json.dumps([
                {"name": "Albuterol Inhaler", "dose": "90mcg", "frequency": "2 puffs as needed for acute shortness of breath", "purpose": "Bronchodilator"},
                {"name": "Fluticasone Propionate Nasal Spray", "dose": "50mcg", "frequency": "1 spray each nostril daily", "purpose": "Nasal Allergy Control"},
                {"name": "Cetirizine", "dose": "10mg", "frequency": "Once daily during pollen season", "purpose": "Antihistamine"}
            ]),
            past_diagnoses=json.dumps(["Acute Sinusitis - Jan 2024", "Childhood Eczema"]),
            family_history=json.dumps(["allergies", "asthma", "migraine"]),
            emergency_contact_name="Robert Smith",
            emergency_contact_phone="+1-555-014-9382",
            emergency_contact_relation="Father"
        )
        db.add(jane_profile)
        
        jane_records = [
            HealthRecord(
                user_id=jane.id,
                record_type="doctor_visit",
                title="Pulmonary Function & Peak Flow Test",
                event_date=datetime.utcnow() - timedelta(days=45),
                doctor_name="Dr. Karen Thorne, MD (Pulmonology)",
                facility="Metro Allergy & Respiratory Institute",
                notes="FEV1 at 88% predicted. Clear lung sounds on auscultation.",
                systolic_bp=116,
                diastolic_bp=74,
                heart_rate=68,
                blood_sugar_fasting=88.0,
                total_cholesterol=165.0,
                hemoglobin=13.2,
                spo2=99.0,
                body_temperature=36.6
            )
        ]
        db.add_all(jane_records)
        
        # ----------------------------------------------------
        # 3. DEMO USER 3: Alex Wong (Healthy baseline young adult)
        # ----------------------------------------------------
        alex = User(
            email="alex.wong@example.com",
            full_name="Alex Wong",
            hashed_password=pw_hash,
            consent_given=True,
            consent_timestamp=datetime.utcnow() - timedelta(days=60)
        )
        db.add(alex)
        db.flush()
        
        alex_profile = HealthProfile(
            user_id=alex.id,
            age=34,
            gender="male",
            blood_group="B+",
            height_cm=178.0,
            weight_kg=73.0,
            bmi=23.04,
            smoking_status="never",
            alcohol_use="occasional",
            physical_activity="active",
            allergies=json.dumps([]),
            chronic_conditions=json.dumps([]),
            current_medications=json.dumps([]),
            past_diagnoses=json.dumps([]),
            family_history=json.dumps([]),
            emergency_contact_name="Emily Wong",
            emergency_contact_phone="+1-555-082-1920",
            emergency_contact_relation="Sister"
        )
        db.add(alex_profile)
        
        alex_records = [
            HealthRecord(
                user_id=alex.id,
                record_type="vital_sign",
                title="Annual Executive Physical & Wellness Panel",
                event_date=datetime.utcnow() - timedelta(days=20),
                doctor_name="Dr. Lisa Chang, MD",
                facility="University Health Wellness Center",
                notes="Patient in excellent health. All metabolic parameters optimal.",
                systolic_bp=118,
                diastolic_bp=76,
                heart_rate=62,
                blood_sugar_fasting=84.0,
                total_cholesterol=160.0,
                hdl_cholesterol=58.0,
                ldl_cholesterol=92.0,
                hemoglobin=15.4,
                spo2=99.0,
                body_temperature=36.7
            )
        ]
        db.add_all(alex_records)
        
        db.commit()
        print("Successfully created 3 demo user profiles with EHR records, vitals series, and predictions!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

# SymptomSense — Multi-Modal Clinical Health Condition Predictor with EHR Synthesis

**SymptomSense** is a full-stack, clinical-grade health assessment web application that estimates possible health conditions by combining a user's **current symptoms** (multi-select & free-text NLP) with their **longitudinal Electronic Health Record (EHR)** history (past diagnoses, chronic illnesses, active medications, family history, and laboratory vitals) using an **explainable Machine Learning** classification engine.

---

## Key Features

1. **JWT-Based Authentication & Private Health Records**
   - Secure email/password authentication with JWT bearer tokens.
   - Private, tenant-isolated Electronic Health Record (EHR) profiles.
   - Instant 1-click Demo Profiles (**John Doe** - Cardiometabolic, **Jane Smith** - Asthma/Allergy, **Alex Wong** - Healthy Baseline).

2. **Electronic Health Record (EHR) Module & Interactive Timeline**
   - Stores demographics, blood group, height, weight, computed BMI with risk classifications.
   - Dynamic tag managers for chronic conditions, allergies, and past diagnoses.
   - Active medication schedule tracker with dosages, frequencies, and purposes.
   - Chronological vertical timeline of doctor visits, lab tests, and attached diagnostic reports (PDF/images).
   - Numerical vitals tracking: Blood Pressure (systolic/diastolic), Fasting & Postprandial Glucose, Total/HDL/LDL Cholesterol, SpO2, Heart Rate, Hemoglobin.

3. **Multi-Modal Symptom Checker & NLP Extractor**
   - Searchable catalog of 240+ categorized medical symptoms across all body systems.
   - Free-form clinical narrative NLP extractor that parses conversational descriptions.
   - Pain/severity slider (1–10 scale), duration selector, and onset type (Sudden vs Gradual).
   - Dynamic EHR Fusion toggle to calibrate predictions against personal health baseline.

4. **Explainable ML Diagnostic Engine (FastAPI & Random Forest / Tree-SHAP)**
   - Trained ensemble Random Forest classifier on 6,000 multi-modal cases across 30 conditions.
   - **99.75% Test Accuracy**, **100% Top-3 Accuracy**, **0.997 5-Fold Cross-Validation Score**.
   - Output: Top-5 probable differential conditions with confidence meters and urgency grading (Low / Medium / High / Emergency).
   - **Tree-SHAP Explainability**: Visual feature importance breakdown showing positive supporting evidence and missing counter-indicators.
   - Recommended next clinical steps, supportive home care protocols, and red-flag warnings.

5. **Clinical Dashboard & Trend Telemetry**
   - Interactive Recharts visualization for dual-line Blood Pressure, Fasting Glucose area charts, and Lipid panels.
   - Symptom frequency horizontal bar analytics.
   - Urgency rating triage distribution pie chart.
   - Interactive daily medication checklist and follow-up reminders.

6. **Safety, Privacy & Emergency Guardian**
   - Prominent clinical disclaimers across all pages.
   - **Emergency Red-Flag Detector** (acute coronary symptoms, FAST stroke signs, respiratory failure) triggering instant 911 / 112 emergency dialer guidance.
   - AES-256 encrypted storage, GDPR/HIPAA-ready consent management, and 1-click **"Delete My Data"** permanent purge option.

7. **HL7 FHIR R4 Interoperability Center**
   - Export full patient health records into standard HL7 FHIR R4 Bundle JSON (Patient, Condition, Observation, MedicationStatement).
   - Import & synchronize external hospital/lab FHIR JSON bundles with LOINC standard coding.

---

## Tech Stack

- **Frontend**: React 18, Vite 5, Tailwind CSS, Lucide Icons, Recharts, jsPDF, html2canvas.
- **Backend**: FastAPI (Python 3.10+ / 3.14), SQLAlchemy, SQLite, Pydantic v2, PyJWT, Bcrypt, Python-Multipart.
- **Machine Learning**: scikit-learn, joblib, pandas, numpy.
- **Interoperability**: HL7 FHIR R4 JSON standard schemas with LOINC code mappings.
- **Testing**: pytest, httpx.

---

## Project Folder Structure

```
aryan-mugdha/
├── backend/
│   ├── app/
│   │   ├── config.py              # Application settings, paths, JWT keys
│   │   ├── database.py            # SQLAlchemy engine, session generator
│   │   ├── main.py                # FastAPI main app, CORS, lifespans, router mounts
│   │   ├── models/                # SQLAlchemy database models
│   │   │   ├── user.py            # User authentication model
│   │   │   ├── profile.py         # Patient health profile & EHR baseline
│   │   │   ├── record.py          # Lab values, visits, timeline records
│   │   │   └── prediction.py      # Symptom checks, ML inferences, notes
│   │   ├── schemas/               # Pydantic validation schemas
│   │   │   ├── auth.py            # Login, register, token, consent
│   │   │   ├── profile.py         # Demographics, allergies, medications
│   │   │   ├── record.py          # Vitals, observations, report uploads
│   │   │   ├── prediction.py      # Symptom requests, responses, explainability
│   │   │   └── fhir.py            # FHIR R4 Bundle, Patient, Observation schemas
│   │   ├── routes/                # FastAPI API endpoints
│   │   │   ├── auth.py            # /api/auth
│   │   │   ├── profile.py         # /api/profile
│   │   │   ├── records.py         # /api/records
│   │   │   ├── predict.py         # /api/predict
│   │   │   ├── analytics.py       # /api/analytics
│   │   │   └── fhir.py            # /api/fhir
│   │   ├── services/              # Business logic & services
│   │   │   ├── auth_service.py    # Bcrypt password hashing, JWT encoding
│   │   │   ├── ml_service.py      # ML model loader, vectorizer, SHAP explainability
│   │   │   ├── red_flags.py       # Emergency red-flag safety detector & NLP
│   │   │   └── fhir_service.py    # FHIR R4 serializer & deserializer
│   │   └── seed.py                # Pre-seeds 3 realistic patient profiles
│   ├── requirements.txt
│   └── uploads/                   # Uploaded medical reports storage
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── context/               # AuthContext & Demo profile switcher
│       ├── components/            # Navbar, Footer, EmergencyModal, ConfidenceBar,
│       │                          # ExplainabilityTree, VitalsChart, FHIRModal, Disclaimer
│       ├── pages/                 # Home, SymptomChecker, ResultsPage, Dashboard,
│       │                          # HealthProfile, EHRTimeline, FHIRHub, PrivacySecurity,
│       │                          # Login, Register
│       └── services/api.js        # Centralized fetch API client
├── ml/
│   ├── generate_dataset.py        # 6,000-case synthetic dataset generator
│   ├── train.py                   # Multi-modal model training & evaluation pipeline
│   ├── dataset/
│   │   ├── disease_symptoms.csv   # Training dataset
│   │   └── disease_metadata.json  # Clinical guidance, ICD-10, actions
│   └── models/
│       ├── symptom_classifier.joblib  # Trained model artifact
│       ├── symptom_list.json          # Searchable symptom catalog
│       ├── feature_metadata.json      # Feature mapping schemas
│       ├── disease_info.json          # Disease clinical guidance
│       └── model_metrics.json         # Accuracy, precision, confusion matrix
├── tests/
│   └── test_symptomsense.py       # Comprehensive pytest suite (auth, EHR, predict, FHIR)
└── README.md
```

---

## Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js v18+ / v20+ and npm

### 2. Backend Setup
```bash
# Navigate to project root
cd aryan-mugdha

# Install Python backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain or regenerate ML models:
python ml/generate_dataset.py
python ml/train.py

# Run FastAPI backend server
uvicorn backend.app.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000` (Interactive Swagger docs at `http://localhost:8000/docs`).

### 3. Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Start Vite dev server
npm run dev
```
Frontend web application will be accessible at `http://localhost:5173`.

---

## Pre-Seeded Demo Accounts

Click the **"Demo Profiles"** dropdown in the navigation header to instantly log in as any of the following:

| Account | Email | Password | Clinical Profile |
| :--- | :--- | :--- | :--- |
| **John Doe** | `john.doe@example.com` | `Password123!` | 58 y/o male with chronic Hypertension, Type 2 Diabetes, Metformin/Amlodipine medications, high BP history. |
| **Jane Smith** | `jane.smith@example.com` | `Password123!` | 28 y/o female with Bronchial Asthma, Allergic Rhinitis, Penicillin allergy, Inhaler history. |
| **Alex Wong** | `alex.wong@example.com` | `Password123!` | 34 y/o male with healthy baseline vitals and no chronic illnesses. |

---

## Running Automated Tests

Run the complete test suite verifying Auth, EHR records, ML predictions, and FHIR export/import:
```bash
pytest tests/test_symptomsense.py -v
```

---

## License & Compliance Notice
This application is created for educational and assistive clinical demonstration purposes. Always seek direct medical consultation from a qualified physician for actual health diagnoses.

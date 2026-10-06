import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

SECRET_KEY = os.getenv("SECRET_KEY", "symptomsense_super_secure_jwt_secret_key_2026_clinical_grade")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/symptomsense.db")

ML_MODEL_PATH = ROOT_DIR / "ml" / "models" / "symptom_classifier.joblib"
DISEASE_INFO_PATH = ROOT_DIR / "ml" / "models" / "disease_info.json"
SYMPTOM_LIST_PATH = ROOT_DIR / "ml" / "models" / "symptom_list.json"
MODEL_METRICS_PATH = ROOT_DIR / "ml" / "models" / "model_metrics.json"

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

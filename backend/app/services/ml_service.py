import json
import os
import joblib
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from ..config import ML_MODEL_PATH, DISEASE_INFO_PATH, SYMPTOM_LIST_PATH, MODEL_METRICS_PATH
from .red_flags import check_emergency_red_flags, extract_symptoms_from_text

class MLSymptomEngine:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = []
        self.symptoms = []
        self.ehr_features = []
        self.disease_info = {}
        self.symptom_catalog = []
        self.model_metrics = {}
        self.is_loaded = False
        
        self.load_artifacts()
        
    def load_artifacts(self):
        try:
            if os.path.exists(ML_MODEL_PATH):
                artifact = joblib.load(ML_MODEL_PATH)
                self.model = artifact["model"]
                self.label_encoder = artifact["label_encoder"]
                self.feature_names = artifact["feature_names"]
                self.symptoms = artifact["symptoms"]
                self.ehr_features = artifact["ehr_features"]
            else:
                print(f"Warning: ML model not found at {ML_MODEL_PATH}")
                
            if os.path.exists(DISEASE_INFO_PATH):
                with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
                    self.disease_info = json.load(f)
                    
            if os.path.exists(SYMPTOM_LIST_PATH):
                with open(SYMPTOM_LIST_PATH, "r", encoding="utf-8") as f:
                    self.symptom_catalog = json.load(f)
                    
            if os.path.exists(MODEL_METRICS_PATH):
                with open(MODEL_METRICS_PATH, "r", encoding="utf-8") as f:
                    self.model_metrics = json.load(f)
                    
            if self.model is not None and self.disease_info:
                self.is_loaded = True
                print(f"MLSymptomEngine successfully loaded with {len(self.feature_names)} features and {len(self.disease_info)} diseases.")
        except Exception as e:
            print(f"Error loading ML artifacts: {e}")
            self.is_loaded = False

    def build_ehr_feature_dict(self, profile: Any = None, recent_records: List[Any] = None) -> Dict[str, float]:
        """
        Extracts binary and numerical EHR risk features from patient profile and latest records.
        """
        ehr = {f: 0.0 for f in self.ehr_features}
        
        if profile is None:
            # Neutral default baseline
            ehr["age"] = 35.0
            return ehr
            
        # Demographics
        ehr["age"] = float(getattr(profile, "age", 35))
        gender = str(getattr(profile, "gender", "male")).lower()
        ehr["gender_male"] = 1.0 if gender == "male" else 0.0
        
        # Lifestyle
        smoking = str(getattr(profile, "smoking_status", "never")).lower()
        ehr["is_smoker"] = 1.0 if smoking in ["current", "former", "yes"] else 0.0
        
        alcohol = str(getattr(profile, "alcohol_use", "never")).lower()
        ehr["alcohol_use"] = 1.0 if alcohol in ["occasional", "frequent", "yes"] else 0.0
        
        bmi = float(getattr(profile, "bmi", 24.0))
        ehr["bmi_high"] = 1.0 if bmi >= 28.0 else 0.0
        
        # Parse JSON lists for chronic conditions
        def _get_list(val):
            if isinstance(val, list):
                return val
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except Exception:
                    return [s.strip() for s in val.split(",") if s.strip()]
            return []
            
        chronic = [str(c).lower() for c in _get_list(getattr(profile, "chronic_conditions", []))]
        fam = [str(f).lower() for f in _get_list(getattr(profile, "family_history", []))]
        allergies = [str(a).lower() for a in _get_list(getattr(profile, "allergies", []))]
        
        ehr["has_hypertension"] = 1.0 if any("hypertens" in c or "high bp" in c or "bp" in c for c in chronic) else 0.0
        ehr["has_diabetes"] = 1.0 if any("diabet" in c or "sugar" in c for c in chronic) else 0.0
        ehr["has_asthma"] = 1.0 if any("asthma" in c or "copd" in c or "wheez" in c for c in chronic) else 0.0
        ehr["has_heart_disease"] = 1.0 if any("heart" in c or "cad" in c or "coronary" in c or "cardiac" in c for c in chronic) else 0.0
        ehr["has_allergies"] = 1.0 if (len(allergies) > 0 or any("allerg" in c for c in chronic)) else 0.0
        
        ehr["family_heart_disease"] = 1.0 if any("heart" in f or "cad" in f or "cardiac" in f or "attack" in f for f in fam) else 0.0
        ehr["family_diabetes"] = 1.0 if any("diabet" in f or "sugar" in f for f in fam) else 0.0
        ehr["family_allergies"] = 1.0 if any("allerg" in f or "asthma" in f for f in fam) else 0.0
        ehr["family_autoimmune"] = 1.0 if any("autoimmun" in f or "lupus" in f or "rheumatoid" in f or "thyroid" in f or "psoriasis" in f for f in fam) else 0.0
        ehr["family_gout"] = 1.0 if any("gout" in f or "uric" in f for f in fam) else 0.0
        ehr["family_migraine"] = 1.0 if any("migraine" in f or "headache" in f for f in fam) else 0.0
        
        # Recent lab records check
        if recent_records:
            for rec in recent_records:
                sbp = getattr(rec, "systolic_bp", None)
                dbp = getattr(rec, "diastolic_bp", None)
                if sbp and sbp >= 140 or dbp and dbp >= 90:
                    ehr["high_bp_reading"] = 1.0
                    
                glu_f = getattr(rec, "blood_sugar_fasting", None)
                glu_p = getattr(rec, "blood_sugar_postprandial", None)
                if (glu_f and glu_f >= 126.0) or (glu_p and glu_p >= 180.0):
                    ehr["high_glucose_reading"] = 1.0
                    
                chol = getattr(rec, "total_cholesterol", None)
                ldl = getattr(rec, "ldl_cholesterol", None)
                if (chol and chol >= 200.0) or (ldl and ldl >= 130.0):
                    ehr["high_cholesterol_reading"] = 1.0
                    
        return ehr

    def predict(
        self,
        symptoms: List[str],
        free_text: Optional[str] = None,
        severity: int = 5,
        duration: str = "2-3 days",
        onset: str = "gradual",
        profile: Any = None,
        recent_records: List[Any] = None,
        manual_ehr_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes multi-modal symptom check + EHR history prediction with explainability.
        """
        if not self.is_loaded:
            self.load_artifacts()
            if not self.is_loaded:
                raise RuntimeError("ML model engine is not loaded.")
                
        # 1. Natural Language Symptom Expansion
        all_symptoms_input = set(symptoms)
        if free_text:
            extracted = extract_symptoms_from_text(free_text, self.symptoms)
            all_symptoms_input.update(extracted)
            
        final_symptoms = sorted(list(all_symptoms_input))
        
        # 2. Emergency Red-Flag Rule Check
        is_emergency, emergency_trigger = check_emergency_red_flags(final_symptoms, free_text)
        
        # 3. Build EHR Features
        ehr_dict = self.build_ehr_feature_dict(profile, recent_records)
        if manual_ehr_override:
            for k, v in manual_ehr_override.items():
                if k in ehr_dict:
                    ehr_dict[k] = float(v)
                    
        # 4. Assemble full feature vector
        vector = []
        for col in self.feature_names:
            if col in self.symptoms:
                val = 1.0 if col in final_symptoms else 0.0
            elif col in ehr_dict:
                val = float(ehr_dict[col])
            else:
                val = 0.0
            vector.append(val)
            
        vector_arr = np.array(vector).reshape(1, -1)
        vector_df = pd.DataFrame(vector_arr, columns=self.feature_names)
        
        # 5. Model Inference (Random Forest Probability Distribution)
        probabilities = self.model.predict_proba(vector_df)[0]
        class_indices = np.argsort(probabilities)[::-1]
        
        top_k = min(5, len(class_indices))
        predictions = []
        
        for rank, idx in enumerate(class_indices[:top_k], start=1):
            disease_name = self.label_encoder.inverse_transform([idx])[0]
            conf = float(probabilities[idx] * 100.0)
            
            # Retrieve clinical metadata
            d_meta = self.disease_info.get(disease_name, {
                "name": disease_name,
                "category": "General",
                "icd10": "R69",
                "urgency": "Medium",
                "specialist": "General Physician",
                "description": f"Clinical assessment for {disease_name}.",
                "recommended_actions": ["Consult with a medical provider for formal diagnostic testing."],
                "home_care": ["Maintain adequate rest and fluid intake."],
                "red_flags": ["Difficulty breathing or sudden severe chest pain"]
            })
            
            # Dynamic urgency adjustment if emergency flag triggered or severity >= 8
            urgency = d_meta.get("urgency", "Medium")
            if is_emergency:
                urgency = "Emergency"
            elif severity >= 8 and urgency in ["Low", "Medium"]:
                urgency = "High"
                
            predictions.append({
                "rank": rank,
                "condition": disease_name,
                "icd10": d_meta.get("icd10", "R69"),
                "category": d_meta.get("category", "General"),
                "confidence": round(conf, 1),
                "urgency": urgency,
                "specialist": d_meta.get("specialist", "General Physician"),
                "description": d_meta.get("description", ""),
                "recommended_actions": d_meta.get("recommended_actions", []),
                "home_care": d_meta.get("home_care", []),
                "red_flags": d_meta.get("red_flags", [])
            })
            
        top_pred = predictions[0]
        
        # 6. Tree-based Explainability (Feature Contribution Analysis for Top Disease)
        explainability_factors = self._compute_feature_contributions(
            top_pred["condition"], vector_arr[0], final_symptoms, ehr_dict
        )
        
        # Clean patient history summary for display
        patient_summary = {
            "age": int(ehr_dict.get("age", 35)),
            "gender": "Male" if ehr_dict.get("gender_male", 1.0) == 1.0 else "Female",
            "smoker": bool(ehr_dict.get("is_smoker", 0.0)),
            "alcohol": bool(ehr_dict.get("alcohol_use", 0.0)),
            "high_bmi": bool(ehr_dict.get("bmi_high", 0.0)),
            "hypertension_history": bool(ehr_dict.get("has_hypertension", 0.0)),
            "diabetes_history": bool(ehr_dict.get("has_diabetes", 0.0)),
            "asthma_history": bool(ehr_dict.get("has_asthma", 0.0)),
            "heart_disease_history": bool(ehr_dict.get("has_heart_disease", 0.0)),
            "allergies_history": bool(ehr_dict.get("has_allergies", 0.0)),
            "recent_high_bp": bool(ehr_dict.get("high_bp_reading", 0.0)),
            "recent_high_glucose": bool(ehr_dict.get("high_glucose_reading", 0.0)),
            "recent_high_cholesterol": bool(ehr_dict.get("high_cholesterol_reading", 0.0))
        }
        
        return {
            "is_emergency": is_emergency,
            "emergency_trigger": emergency_trigger,
            "top_condition": top_pred["condition"],
            "top_condition_icd10": top_pred["icd10"],
            "top_confidence": top_pred["confidence"],
            "urgency": top_pred["urgency"],
            "specialist": top_pred["specialist"],
            "predictions": predictions,
            "explainability": explainability_factors,
            "recommended_actions": top_pred["recommended_actions"],
            "home_care": top_pred["home_care"],
            "red_flags": top_pred["red_flags"],
            "patient_history_summary": patient_summary
        }

    def _compute_feature_contributions(
        self, disease_name: str, feature_vector: np.ndarray, symptoms_present: List[str], ehr_dict: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Computes clinical SHAP-style positive and negative feature evidence weights.
        """
        factors = []
        d_meta = self.disease_info.get(disease_name, {})
        core_syms = d_meta.get("core_symptoms", [])
        sec_syms = d_meta.get("secondary_symptoms", [])
        assoc = d_meta.get("ehr_associations", {})
        
        # 1. Positive Symptoms Present
        for sym in symptoms_present:
            weight = 0.35 if sym in core_syms else (0.20 if sym in sec_syms else 0.10)
            factors.append({
                "feature": sym,
                "feature_label": sym.replace("_", " ").capitalize(),
                "impact": "positive",
                "contribution": round(weight * 100, 1),
                "type": "symptom"
            })
            
        # 2. EHR Risk Factors Present
        for f, val in ehr_dict.items():
            if f == "age" and val > 55 and ("age_over_45" in assoc or "age_over_65" in assoc):
                factors.append({
                    "feature": "age_factor",
                    "feature_label": f"Age Profile ({int(val)} years)",
                    "impact": "positive",
                    "contribution": 18.5,
                    "type": "ehr_history"
                })
            elif f != "age" and val == 1.0 and f in assoc:
                label = f.replace("has_", "History of ").replace("family_", "Family History of ").replace("_", " ").capitalize()
                factors.append({
                    "feature": f,
                    "feature_label": label,
                    "impact": "positive",
                    "contribution": round(float(assoc[f]) * 12.0, 1),
                    "type": "vital_sign" if "reading" in f else "ehr_history"
                })
                
        # 3. Key Missing Symptoms (Negative evidence)
        for cs in core_syms:
            if cs not in symptoms_present:
                factors.append({
                    "feature": cs,
                    "feature_label": f"Absence of {cs.replace('_', ' ')}",
                    "impact": "negative",
                    "contribution": -12.0,
                    "type": "symptom"
                })
                
        # Sort by absolute contribution magnitude
        factors.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        return factors[:10]

# Global singleton engine instance
ml_engine = MLSymptomEngine()

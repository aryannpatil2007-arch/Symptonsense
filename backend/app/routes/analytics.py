import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import HealthProfile
from ..models.record import HealthRecord
from ..models.prediction import SymptomPrediction
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Dashboard"])

@router.get("/dashboard")
def get_dashboard_analytics(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # 1. Fetch user profile
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    
    # 2. Fetch all records chronologically
    records = db.query(HealthRecord).filter(HealthRecord.user_id == user.id).order_by(HealthRecord.event_date.asc()).all()
    
    # 3. Fetch all predictions
    predictions = db.query(SymptomPrediction).filter(SymptomPrediction.user_id == user.id).order_by(SymptomPrediction.created_at.desc()).all()
    
    # --- Vitals History Series ---
    bp_series = []
    glucose_series = []
    cholesterol_series = []
    spo2_series = []
    
    for r in records:
        date_str = r.event_date.strftime("%b %d, %Y") if r.event_date else "Unknown"
        
        if r.systolic_bp is not None and r.diastolic_bp is not None:
            bp_series.append({
                "date": date_str,
                "systolic": r.systolic_bp,
                "diastolic": r.diastolic_bp,
                "heart_rate": r.heart_rate or 72
            })
            
        if r.blood_sugar_fasting is not None or r.blood_sugar_postprandial is not None:
            glucose_series.append({
                "date": date_str,
                "fasting": r.blood_sugar_fasting,
                "postprandial": r.blood_sugar_postprandial
            })
            
        if r.total_cholesterol is not None or r.ldl_cholesterol is not None:
            cholesterol_series.append({
                "date": date_str,
                "total": r.total_cholesterol,
                "ldl": r.ldl_cholesterol,
                "hdl": r.hdl_cholesterol
            })
            
        if r.spo2 is not None:
            spo2_series.append({
                "date": date_str,
                "spo2": r.spo2
            })
            
    # --- Symptom Frequencies ---
    symptom_counter = {}
    urgency_counts = {"Low": 0, "Medium": 0, "High": 0, "Emergency": 0}
    
    for p in predictions:
        urg = p.urgency if p.urgency in urgency_counts else "Medium"
        urgency_counts[urg] += 1
        
        try:
            syms = json.loads(p.symptoms_selected) if isinstance(p.symptoms_selected, str) else p.symptoms_selected
            for s in syms:
                label = s.replace("_", " ").capitalize()
                symptom_counter[label] = symptom_counter.get(label, 0) + 1
        except Exception:
            pass
            
    top_symptoms_chart = [
        {"name": k, "count": v}
        for k, v in sorted(symptom_counter.items(), key=lambda x: x[1], reverse=True)[:8]
    ]
    
    # --- Medication & Follow-up Reminders ---
    reminders = []
    if profile:
        try:
            meds = json.loads(profile.current_medications) if isinstance(profile.current_medications, str) else profile.current_medications
            for med in meds:
                name = med.get("name") if isinstance(med, dict) else str(med)
                dose = med.get("dose", "As prescribed") if isinstance(med, dict) else ""
                reminders.append({
                    "id": f"med-{name}",
                    "type": "medication",
                    "title": f"Take {name}",
                    "description": f"Dosage: {dose}",
                    "due": "Daily morning / evening"
                })
        except Exception:
            pass
            
    if len(predictions) > 0:
        latest_p = predictions[0]
        if latest_p.urgency in ["High", "Emergency"]:
            reminders.append({
                "id": "urgent-followup",
                "type": "clinical_alert",
                "title": f"Follow-up for {latest_p.top_condition}",
                "description": f"Recommended consultation with {latest_p.specialist or 'Doctor'}.",
                "due": "Immediate / Within 24 hours"
            })
            
    # --- Latest Vitals Snapshot ---
    latest_bp = bp_series[-1] if bp_series else None
    latest_glucose = glucose_series[-1] if glucose_series else None
    latest_cholesterol = cholesterol_series[-1] if cholesterol_series else None
    
    return {
        "summary": {
            "total_records": len(records),
            "total_assessments": len(predictions),
            "latest_assessment": predictions[0].top_condition if predictions else "None",
            "latest_urgency": predictions[0].urgency if predictions else "None",
            "latest_check_date": predictions[0].created_at.strftime("%b %d, %Y") if predictions else None
        },
        "vitals": {
            "latest_bp": latest_bp,
            "latest_glucose": latest_glucose,
            "latest_cholesterol": latest_cholesterol,
            "bp_series": bp_series,
            "glucose_series": glucose_series,
            "cholesterol_series": cholesterol_series,
            "spo2_series": spo2_series
        },
        "symptom_frequency": top_symptoms_chart,
        "urgency_distribution": [
            {"name": "Low", "value": urgency_counts["Low"], "color": "#10B981"},
            {"name": "Medium", "value": urgency_counts["Medium"], "color": "#F59E0B"},
            {"name": "High", "value": urgency_counts["High"], "color": "#EF4444"},
            {"name": "Emergency", "value": urgency_counts["Emergency"], "color": "#DC2626"}
        ],
        "reminders": reminders
    }

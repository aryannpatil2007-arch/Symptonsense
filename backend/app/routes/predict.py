import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import HealthProfile
from ..models.record import HealthRecord
from ..models.prediction import SymptomPrediction
from ..schemas.prediction import SymptomCheckRequest, SymptomPredictionResponse, SymptomPredictionOut
from ..services.auth_service import get_optional_current_user, get_current_user
from ..services.ml_service import ml_engine

router = APIRouter(prefix="/api/predict", tags=["ML Prediction Engine"])

@router.get("/symptoms-list")
def get_symptoms_list():
    """
    Returns full categorized dictionary of medical symptoms for searchable multi-select UI.
    """
    return {
        "total": len(ml_engine.symptom_catalog),
        "symptoms": ml_engine.symptom_catalog
    }

@router.get("/metrics")
def get_model_metrics():
    """
    Returns transparency report: ML accuracy, precision, recall, confusion matrix, top features.
    """
    return ml_engine.model_metrics

@router.post("", response_model=SymptomPredictionResponse)
def run_symptom_prediction(
    request: SymptomCheckRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    profile = None
    recent_records = []
    
    if current_user and request.include_profile_history:
        profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
        recent_records = db.query(HealthRecord).filter(HealthRecord.user_id == current_user.id).order_by(HealthRecord.event_date.desc()).limit(10).all()
        
    result = ml_engine.predict(
        symptoms=request.symptoms,
        free_text=request.description,
        severity=request.severity,
        duration=request.duration,
        onset=request.onset,
        profile=profile,
        recent_records=recent_records,
        manual_ehr_override=request.manual_ehr_override
    )
    
    saved_id = None
    created_at = datetime.utcnow()
    
    # Save to user history if authenticated
    if current_user:
        prediction_record = SymptomPrediction(
            user_id=current_user.id,
            symptoms_selected=json.dumps(request.symptoms),
            symptom_description=request.description,
            severity=request.severity,
            duration=request.duration,
            onset=request.onset,
            is_emergency=result["is_emergency"],
            emergency_trigger=result["emergency_trigger"],
            top_condition=result["top_condition"],
            top_condition_icd10=result["top_condition_icd10"],
            top_confidence=result["top_confidence"],
            urgency=result["urgency"],
            specialist=result["specialist"],
            all_predictions=json.dumps(result["predictions"]),
            explainability=json.dumps(result["explainability"]),
            recommended_actions=json.dumps(result["recommended_actions"]),
            home_care=json.dumps(result["home_care"]),
            red_flags=json.dumps(result["red_flags"]),
            created_at=created_at
        )
        db.add(prediction_record)
        db.commit()
        db.refresh(prediction_record)
        saved_id = prediction_record.id
        
    result["id"] = saved_id
    result["created_at"] = created_at
    return result

@router.get("/history", response_model=List[SymptomPredictionOut])
def get_prediction_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(SymptomPrediction).filter(SymptomPrediction.user_id == user.id).order_by(SymptomPrediction.created_at.desc()).all()
    
    def _parse(val):
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return []
        return []
        
    out = []
    for item in history:
        out.append(SymptomPredictionOut(
            id=item.id,
            user_id=item.user_id,
            symptoms_selected=_parse(item.symptoms_selected),
            symptom_description=item.symptom_description,
            severity=item.severity,
            duration=item.duration,
            onset=item.onset,
            is_emergency=item.is_emergency,
            emergency_trigger=item.emergency_trigger,
            top_condition=item.top_condition,
            top_condition_icd10=item.top_condition_icd10,
            top_confidence=item.top_confidence,
            urgency=item.urgency,
            specialist=item.specialist,
            all_predictions=_parse(item.all_predictions),
            explainability=_parse(item.explainability),
            recommended_actions=_parse(item.recommended_actions),
            home_care=_parse(item.home_care),
            red_flags=_parse(item.red_flags),
            created_at=item.created_at
        ))
    return out

@router.get("/{prediction_id}", response_model=SymptomPredictionOut)
def get_prediction_by_id(
    prediction_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(SymptomPrediction).filter(SymptomPrediction.id == prediction_id, SymptomPrediction.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Prediction assessment not found.")
        
    def _parse(val):
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return []
        return []
        
    return SymptomPredictionOut(
        id=item.id,
        user_id=item.user_id,
        symptoms_selected=_parse(item.symptoms_selected),
        symptom_description=item.symptom_description,
        severity=item.severity,
        duration=item.duration,
        onset=item.onset,
        is_emergency=item.is_emergency,
        emergency_trigger=item.emergency_trigger,
        top_condition=item.top_condition,
        top_condition_icd10=item.top_condition_icd10,
        top_confidence=item.top_confidence,
        urgency=item.urgency,
        specialist=item.specialist,
        all_predictions=_parse(item.all_predictions),
        explainability=_parse(item.explainability),
        recommended_actions=_parse(item.recommended_actions),
        home_care=_parse(item.home_care),
        red_flags=_parse(item.red_flags),
        created_at=item.created_at
    )

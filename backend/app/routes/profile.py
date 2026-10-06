import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import HealthProfile
from ..schemas.profile import HealthProfileUpdate, HealthProfileOut
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Health Profile"])

def _format_profile_out(profile: HealthProfile) -> HealthProfileOut:
    def _parse(val):
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return [s.strip() for s in val.split(",") if s.strip()]
        return []

    return HealthProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        age=profile.age,
        gender=profile.gender,
        blood_group=profile.blood_group,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        bmi=profile.bmi,
        smoking_status=profile.smoking_status,
        alcohol_use=profile.alcohol_use,
        physical_activity=profile.physical_activity,
        allergies=_parse(profile.allergies),
        chronic_conditions=_parse(profile.chronic_conditions),
        current_medications=_parse(profile.current_medications),
        past_diagnoses=_parse(profile.past_diagnoses),
        family_history=_parse(profile.family_history),
        emergency_contact_name=profile.emergency_contact_name,
        emergency_contact_phone=profile.emergency_contact_phone,
        emergency_contact_relation=profile.emergency_contact_relation,
        updated_at=profile.updated_at
    )

@router.get("", response_model=HealthProfileOut)
def get_health_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    if not profile:
        profile = HealthProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return _format_profile_out(profile)

@router.put("", response_model=HealthProfileOut)
def update_health_profile(profile_in: HealthProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    if not profile:
        profile = HealthProfile(user_id=user.id)
        db.add(profile)
        
    profile.age = profile_in.age
    profile.gender = profile_in.gender
    profile.blood_group = profile_in.blood_group
    profile.height_cm = profile_in.height_cm
    profile.weight_kg = profile_in.weight_kg
    
    # Recalculate BMI
    if profile.height_cm > 0:
        height_m = profile.height_cm / 100.0
        profile.bmi = round(profile.weight_kg / (height_m * height_m), 2)
        
    profile.smoking_status = profile_in.smoking_status
    profile.alcohol_use = profile_in.alcohol_use
    profile.physical_activity = profile_in.physical_activity
    
    profile.allergies = json.dumps(profile_in.allergies)
    profile.chronic_conditions = json.dumps(profile_in.chronic_conditions)
    profile.current_medications = json.dumps(profile_in.current_medications)
    profile.past_diagnoses = json.dumps(profile_in.past_diagnoses)
    profile.family_history = json.dumps(profile_in.family_history)
    
    profile.emergency_contact_name = profile_in.emergency_contact_name
    profile.emergency_contact_phone = profile_in.emergency_contact_phone
    profile.emergency_contact_relation = profile_in.emergency_contact_relation
    
    db.commit()
    db.refresh(profile)
    return _format_profile_out(profile)

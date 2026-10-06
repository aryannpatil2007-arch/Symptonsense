from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import HealthProfile
from ..models.record import HealthRecord
from ..models.prediction import SymptomPrediction
from ..schemas.fhir import FHIRImportRequest, FHIRImportResponse
from ..services.auth_service import get_current_user
from ..services.fhir_service import export_fhir_bundle, import_fhir_bundle

router = APIRouter(prefix="/api/fhir", tags=["FHIR Interoperability"])

@router.get("/export")
def export_user_fhir_bundle(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exports full patient electronic health records in HL7 FHIR R4 standard JSON format.
    """
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    records = db.query(HealthRecord).filter(HealthRecord.user_id == user.id).all()
    predictions = db.query(SymptomPrediction).filter(SymptomPrediction.user_id == user.id).all()
    
    bundle = export_fhir_bundle(user=user, profile=profile, records=records, predictions=predictions)
    
    return JSONResponse(
        content=bundle,
        headers={"Content-Disposition": f"attachment; filename=symptomsense_fhir_patient_{user.id}.json"}
    )

@router.post("/import", response_model=FHIRImportResponse)
def import_user_fhir_bundle(
    payload: FHIRImportRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Imports and synchronizes FHIR R4 Bundle data into the patient's EHR profile and records.
    """
    try:
        res = import_fhir_bundle(bundle_data=payload.bundle, user=user, db=db)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"FHIR Import failed: {str(e)}")

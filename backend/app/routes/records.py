import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from ..config import UPLOAD_DIR
from ..database import get_db
from ..models.user import User
from ..models.record import HealthRecord
from ..schemas.record import HealthRecordCreate, HealthRecordOut
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/records", tags=["Health Records & EHR Timeline"])

@router.get("", response_model=List[HealthRecordOut])
def get_user_records(
    record_type: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(HealthRecord).filter(HealthRecord.user_id == user.id)
    if record_type:
        query = query.filter(HealthRecord.record_type == record_type)
    records = query.order_by(HealthRecord.event_date.desc()).all()
    return records

@router.post("", response_model=HealthRecordOut, status_code=status.HTTP_201_CREATED)
def create_health_record(
    record_in: HealthRecordCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event_dt = record_in.event_date if record_in.event_date else datetime.utcnow()
    new_rec = HealthRecord(
        user_id=user.id,
        record_type=record_in.record_type,
        title=record_in.title,
        event_date=event_dt,
        doctor_name=record_in.doctor_name,
        facility=record_in.facility,
        notes=record_in.notes,
        systolic_bp=record_in.systolic_bp,
        diastolic_bp=record_in.diastolic_bp,
        heart_rate=record_in.heart_rate,
        blood_sugar_fasting=record_in.blood_sugar_fasting,
        blood_sugar_postprandial=record_in.blood_sugar_postprandial,
        total_cholesterol=record_in.total_cholesterol,
        hdl_cholesterol=record_in.hdl_cholesterol,
        ldl_cholesterol=record_in.ldl_cholesterol,
        hemoglobin=record_in.hemoglobin,
        spo2=record_in.spo2,
        body_temperature=record_in.body_temperature,
        file_url=record_in.file_url,
        file_name=record_in.file_name,
        file_size_bytes=record_in.file_size_bytes,
        fhir_resource_type=record_in.fhir_resource_type or "Observation"
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec

@router.post("/upload", response_model=HealthRecordOut)
async def upload_medical_report(
    title: str = Form(...),
    record_type: str = Form("document_upload"),
    doctor_name: Optional[str] = Form(None),
    facility: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    event_date: Optional[str] = Form(None),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save file to upload directory
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{user.id}_{uuid.uuid4().hex[:10]}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
        
    parsed_date = datetime.utcnow()
    if event_date:
        try:
            parsed_date = datetime.fromisoformat(event_date.replace("Z", ""))
        except Exception:
            pass
            
    new_rec = HealthRecord(
        user_id=user.id,
        record_type=record_type,
        title=title,
        event_date=parsed_date,
        doctor_name=doctor_name,
        facility=facility,
        notes=notes,
        file_url=f"/uploads/{unique_filename}",
        file_name=file.filename,
        file_size_bytes=len(content),
        fhir_resource_type="DiagnosticReport"
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec

@router.delete("/{record_id}", status_code=status.HTTP_200_OK)
def delete_health_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(HealthRecord).filter(HealthRecord.id == record_id, HealthRecord.user_id == user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found.")
        
    db.delete(rec)
    db.commit()
    return {"status": "success", "message": "Record successfully removed."}

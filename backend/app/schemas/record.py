from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class HealthRecordCreate(BaseModel):
    record_type: str = "lab_result"  # lab_result, doctor_visit, vital_sign, document_upload
    title: str = Field(..., min_length=2, max_length=150)
    event_date: Optional[datetime] = None
    doctor_name: Optional[str] = None
    facility: Optional[str] = None
    notes: Optional[str] = None
    
    # Numerical lab & vital fields
    systolic_bp: Optional[int] = Field(None, ge=50, le=280)
    diastolic_bp: Optional[int] = Field(None, ge=30, le=180)
    heart_rate: Optional[int] = Field(None, ge=30, le=250)
    blood_sugar_fasting: Optional[float] = Field(None, ge=20.0, le=800.0)
    blood_sugar_postprandial: Optional[float] = Field(None, ge=20.0, le=800.0)
    total_cholesterol: Optional[float] = Field(None, ge=50.0, le=600.0)
    hdl_cholesterol: Optional[float] = Field(None, ge=10.0, le=150.0)
    ldl_cholesterol: Optional[float] = Field(None, ge=20.0, le=400.0)
    hemoglobin: Optional[float] = Field(None, ge=3.0, le=25.0)
    spo2: Optional[float] = Field(None, ge=50.0, le=100.0)
    body_temperature: Optional[float] = Field(None, ge=30.0, le=45.0)
    
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size_bytes: Optional[int] = None
    fhir_resource_type: Optional[str] = "Observation"

class HealthRecordOut(HealthRecordCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

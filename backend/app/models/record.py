from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Record Category & Meta
    record_type = Column(String, default="lab_result") # lab_result, doctor_visit, vital_sign, document_upload
    title = Column(String, nullable=False)
    event_date = Column(DateTime, default=datetime.utcnow, index=True)
    doctor_name = Column(String, nullable=True)
    facility = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Numerical Lab Values & Vital Signs
    systolic_bp = Column(Integer, nullable=True)          # mmHg (e.g., 120)
    diastolic_bp = Column(Integer, nullable=True)         # mmHg (e.g., 80)
    heart_rate = Column(Integer, nullable=True)           # bpm (e.g., 72)
    blood_sugar_fasting = Column(Float, nullable=True)    # mg/dL (e.g., 95.0)
    blood_sugar_postprandial = Column(Float, nullable=True)# mg/dL (e.g., 130.0)
    total_cholesterol = Column(Float, nullable=True)      # mg/dL (e.g., 190.0)
    hdl_cholesterol = Column(Float, nullable=True)        # mg/dL (e.g., 55.0)
    ldl_cholesterol = Column(Float, nullable=True)        # mg/dL (e.g., 110.0)
    hemoglobin = Column(Float, nullable=True)             # g/dL (e.g., 14.5)
    spo2 = Column(Float, nullable=True)                   # % (e.g., 98.0)
    body_temperature = Column(Float, nullable=True)       # Celsius (e.g., 36.8)
    
    # Attached Report / File info
    file_url = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    
    # FHIR Mapping Tag
    fhir_resource_type = Column(String, default="Observation")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="records")

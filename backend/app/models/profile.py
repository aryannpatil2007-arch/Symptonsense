from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Demographics & Body metrics
    age = Column(Integer, default=30)
    gender = Column(String, default="male")  # male, female, other
    blood_group = Column(String, default="O+")
    height_cm = Column(Float, default=172.0)
    weight_kg = Column(Float, default=70.0)
    bmi = Column(Float, default=23.66)
    
    # Lifestyle
    smoking_status = Column(String, default="never")  # never, former, current
    alcohol_use = Column(String, default="never")      # never, occasional, frequent
    physical_activity = Column(String, default="moderate")  # sedentary, moderate, active
    
    # Clinical history stored as JSON serialized strings
    allergies = Column(Text, default="[]")                # e.g. ["Penicillin", "Peanuts"]
    chronic_conditions = Column(Text, default="[]")       # e.g. ["Hypertension", "Asthma"]
    current_medications = Column(Text, default="[]")      # e.g. [{"name": "Metformin", "dose": "500mg"}]
    past_diagnoses = Column(Text, default="[]")           # e.g. ["COVID-19 in 2022"]
    family_history = Column(Text, default="[]")           # e.g. ["heart_disease", "diabetes"]
    
    # Emergency Contact
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relation = Column(String, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")

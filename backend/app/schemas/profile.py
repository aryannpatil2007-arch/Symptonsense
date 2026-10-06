from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class MedicationItem(BaseModel):
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    purpose: Optional[str] = None

class HealthProfileBase(BaseModel):
    age: int = Field(30, ge=0, le=125)
    gender: str = "male"
    blood_group: str = "O+"
    height_cm: float = Field(170.0, ge=40.0, le=260.0)
    weight_kg: float = Field(70.0, ge=2.0, le=350.0)
    smoking_status: str = "never"  # never, former, current
    alcohol_use: str = "never"      # never, occasional, frequent
    physical_activity: str = "moderate"  # sedentary, moderate, active
    allergies: List[str] = []
    chronic_conditions: List[str] = []
    current_medications: List[Dict[str, Any]] = []
    past_diagnoses: List[str] = []
    family_history: List[str] = []
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None

class HealthProfileUpdate(HealthProfileBase):
    pass

class HealthProfileOut(HealthProfileBase):
    id: int
    user_id: int
    bmi: float
    updated_at: datetime

    class Config:
        from_attributes = True

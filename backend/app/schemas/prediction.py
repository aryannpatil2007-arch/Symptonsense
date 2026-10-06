from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SymptomCheckRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1)
    description: Optional[str] = None
    severity: int = Field(5, ge=1, le=10)
    duration: str = "2-3 days"
    onset: str = "gradual"  # sudden, gradual
    include_profile_history: bool = True
    manual_ehr_override: Optional[Dict[str, Any]] = None  # Optional guest override

class ConditionPrediction(BaseModel):
    rank: int
    condition: str
    icd10: str
    category: str
    confidence: float # percentage 0 to 100
    urgency: str # Low, Medium, High, Emergency
    specialist: str
    description: str
    recommended_actions: List[str]
    home_care: List[str]
    red_flags: List[str]

class ExplainabilityFactor(BaseModel):
    feature: str
    feature_label: str
    impact: str # "positive" (increases risk/match) or "negative"
    contribution: float # absolute/relative weight
    type: str # "symptom" or "ehr_history" or "vital_sign"

class SymptomPredictionResponse(BaseModel):
    id: Optional[int] = None
    is_emergency: bool
    emergency_trigger: Optional[str] = None
    top_condition: str
    top_condition_icd10: str
    top_confidence: float
    urgency: str
    specialist: str
    predictions: List[ConditionPrediction]
    explainability: List[ExplainabilityFactor]
    recommended_actions: List[str]
    home_care: List[str]
    red_flags: List[str]
    patient_history_summary: Dict[str, Any]
    created_at: Optional[datetime] = None

class SymptomPredictionOut(BaseModel):
    id: int
    user_id: int
    symptoms_selected: List[str]
    symptom_description: Optional[str] = None
    severity: int
    duration: str
    onset: str
    is_emergency: bool
    emergency_trigger: Optional[str] = None
    top_condition: str
    top_condition_icd10: Optional[str] = None
    top_confidence: float
    urgency: str
    specialist: Optional[str] = None
    all_predictions: List[Dict[str, Any]]
    explainability: List[Dict[str, Any]]
    recommended_actions: List[str]
    home_care: List[str]
    red_flags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

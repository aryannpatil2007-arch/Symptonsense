from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class SymptomPrediction(Base):
    __tablename__ = "symptom_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Input Symptoms & Characteristics
    symptoms_selected = Column(Text, nullable=False) # JSON list e.g. ["cough", "fever"]
    symptom_description = Column(Text, nullable=True) # Free-form narrative
    severity = Column(Integer, default=5)            # 1 to 10 scale
    duration = Column(String, default="2-3 days")    # e.g., "1 week"
    onset = Column(String, default="gradual")        # sudden, gradual
    is_emergency = Column(Boolean, default=False)
    emergency_trigger = Column(String, nullable=True)
    
    # Prediction Outputs
    top_condition = Column(String, nullable=False)
    top_condition_icd10 = Column(String, nullable=True)
    top_confidence = Column(Float, nullable=False)    # 0.0 to 100.0 percentage
    urgency = Column(String, default="Low")          # Low, Medium, High, Emergency
    specialist = Column(String, nullable=True)
    
    # Full Model Explanations & Array
    all_predictions = Column(Text, nullable=False)   # JSON array of top-5 predictions
    explainability = Column(Text, nullable=False)    # JSON feature importance breakdown
    recommended_actions = Column(Text, nullable=True)# JSON list of actions
    home_care = Column(Text, nullable=True)          # JSON list of remedies
    red_flags = Column(Text, nullable=True)          # JSON list of red flags
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="predictions")

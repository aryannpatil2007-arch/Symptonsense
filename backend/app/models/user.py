from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="patient")
    consent_given = Column(Boolean, default=True)
    consent_timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("HealthProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    records = relationship("HealthRecord", back_populates="user", cascade="all, delete-orphan")
    predictions = relationship("SymptomPrediction", back_populates="user", cascade="all, delete-orphan")

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import UPLOAD_DIR
from .database import engine, Base
from .seed import seed_database
from .routes import (
    auth_router,
    profile_router,
    records_router,
    predict_router,
    analytics_router,
    fhir_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed demo data
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(
    title="SymptomSense API",
    description="Clinical-Grade Multi-Modal Symptom Checker with EHR Integration & Explainable ML",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS for Vite React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static medical document access
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Include API Routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(records_router)
app.include_router(predict_router)
app.include_router(analytics_router)
app.include_router(fhir_router)

@app.get("/")
def root():
    return {
        "name": "SymptomSense API",
        "status": "online",
        "version": "2.0.0",
        "docs": "/docs",
        "description": "Multi-Modal Health Condition Prediction combining active symptoms with patient EHR history."
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "SymptomSense Backend & ML Engine"}

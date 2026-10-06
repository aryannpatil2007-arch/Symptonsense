from .auth import router as auth_router
from .profile import router as profile_router
from .records import router as records_router
from .predict import router as predict_router
from .analytics import router as analytics_router
from .fhir import router as fhir_router

__all__ = [
    "auth_router",
    "profile_router",
    "records_router",
    "predict_router",
    "analytics_router",
    "fhir_router"
]

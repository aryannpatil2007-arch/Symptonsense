from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class FHIRIdentifier(BaseModel):
    system: str = "http://symptomsense.ai/identifiers"
    value: str

class FHIRCodeableConcept(BaseModel):
    coding: List[Dict[str, Any]]
    text: str

class FHIRPatientResource(BaseModel):
    resourceType: str = "Patient"
    id: str
    identifier: Optional[List[FHIRIdentifier]] = None
    active: bool = True
    name: List[Dict[str, Any]]
    gender: str
    birthDate: Optional[str] = None
    telecom: Optional[List[Dict[str, str]]] = None

class FHIREntry(BaseModel):
    fullUrl: str
    resource: Dict[str, Any]

class FHIRBundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "collection"
    entry: List[FHIREntry]

class FHIRImportRequest(BaseModel):
    bundle: Dict[str, Any]

class FHIRImportResponse(BaseModel):
    status: str
    records_imported: int
    profile_updated: bool
    details: List[str]

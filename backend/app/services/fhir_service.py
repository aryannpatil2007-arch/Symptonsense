import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.profile import HealthProfile
from ..models.record import HealthRecord
from ..models.prediction import SymptomPrediction

LOINC_CODES = {
    "systolic_bp": {"code": "8480-6", "display": "Systolic blood pressure", "unit": "mmHg"},
    "diastolic_bp": {"code": "8462-4", "display": "Diastolic blood pressure", "unit": "mmHg"},
    "blood_sugar_fasting": {"code": "1558-6", "display": "Fasting blood glucose", "unit": "mg/dL"},
    "blood_sugar_postprandial": {"code": "1521-4", "display": "Postprandial glucose", "unit": "mg/dL"},
    "total_cholesterol": {"code": "2093-3", "display": "Total cholesterol", "unit": "mg/dL"},
    "hdl_cholesterol": {"code": "2085-9", "display": "HDL cholesterol", "unit": "mg/dL"},
    "ldl_cholesterol": {"code": "2089-1", "display": "LDL cholesterol", "unit": "mg/dL"},
    "hemoglobin": {"code": "718-7", "display": "Hemoglobin", "unit": "g/dL"},
    "spo2": {"code": "2708-6", "display": "Oxygen saturation in Arterial blood", "unit": "%"},
    "heart_rate": {"code": "8867-4", "display": "Heart rate", "unit": "beats/minute"},
    "bmi": {"code": "39156-5", "display": "Body mass index", "unit": "kg/m2"}
}

def export_fhir_bundle(user: User, profile: Optional[HealthProfile], records: List[HealthRecord], predictions: List[SymptomPrediction]) -> Dict[str, Any]:
    """
    Exports full patient electronic health record into standard HL7 FHIR R4 Bundle JSON format.
    """
    bundle_id = f"urn:uuid:{uuid.uuid4()}"
    patient_ref_id = f"patient-{user.id}"
    
    entries = []
    
    # 1. FHIR Resource: Patient
    patient_resource = {
        "resourceType": "Patient",
        "id": patient_ref_id,
        "identifier": [
            {
                "system": "http://symptomsense.ai/patients",
                "value": f"SS-PAT-{user.id:06d}"
            }
        ],
        "active": True,
        "name": [
            {
                "use": "official",
                "text": user.full_name
            }
        ],
        "telecom": [
            {
                "system": "email",
                "value": user.email,
                "use": "home"
            }
        ],
        "gender": getattr(profile, "gender", "unknown") if profile else "unknown",
        "extension": [
            {
                "url": "http://symptomsense.ai/fhir/StructureDefinition/blood-group",
                "valueString": getattr(profile, "blood_group", "O+") if profile else "O+"
            },
            {
                "url": "http://symptomsense.ai/fhir/StructureDefinition/smoking-status",
                "valueString": getattr(profile, "smoking_status", "never") if profile else "never"
            }
        ]
    }
    
    entries.append({
        "fullUrl": f"urn:uuid:{uuid.uuid4()}",
        "resource": patient_resource
    })
    
    # 2. FHIR Resource: Chronic Conditions & Past Diagnoses
    if profile:
        def _parse(field):
            if isinstance(field, list):
                return field
            if isinstance(field, str):
                try:
                    return json.loads(field)
                except Exception:
                    return [s.strip() for s in field.split(",") if s.strip()]
            return []
            
        chronic = _parse(profile.chronic_conditions)
        for cond_name in chronic:
            cond_res = {
                "resourceType": "Condition",
                "id": f"cond-{uuid.uuid4().hex[:8]}",
                "clinicalStatus": {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
                },
                "verificationStatus": {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]
                },
                "category": [
                    {
                        "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "problem-list-item", "display": "Problem List Item"}]
                    }
                ],
                "code": {
                    "text": str(cond_name)
                },
                "subject": {
                    "reference": f"Patient/{patient_ref_id}",
                    "display": user.full_name
                },
                "recordedDate": datetime.utcnow().strftime("%Y-%m-%d")
            }
            entries.append({"fullUrl": f"urn:uuid:{uuid.uuid4()}", "resource": cond_res})
            
        # 3. FHIR Resource: MedicationStatement
        meds = _parse(profile.current_medications)
        for med in meds:
            med_name = med.get("name") if isinstance(med, dict) else str(med)
            dose_info = med.get("dose", "") if isinstance(med, dict) else ""
            freq_info = med.get("frequency", "") if isinstance(med, dict) else ""
            med_res = {
                "resourceType": "MedicationStatement",
                "id": f"med-{uuid.uuid4().hex[:8]}",
                "status": "active",
                "medicationCodeableConcept": {
                    "text": med_name
                },
                "subject": {
                    "reference": f"Patient/{patient_ref_id}",
                    "display": user.full_name
                },
                "dosage": [
                    {
                        "text": f"{dose_info} {freq_info}".strip()
                    }
                ]
            }
            entries.append({"fullUrl": f"urn:uuid:{uuid.uuid4()}", "resource": med_res})
            
    # 4. FHIR Resource: Observation (Vitals and Lab Results)
    for rec in records:
        event_iso = rec.event_date.isoformat() if rec.event_date else datetime.utcnow().isoformat()
        
        # Check numeric lab attributes
        for attr, l_info in LOINC_CODES.items():
            val = getattr(rec, attr, None)
            if val is not None:
                obs_res = {
                    "resourceType": "Observation",
                    "id": f"obs-{uuid.uuid4().hex[:8]}",
                    "status": "final",
                    "category": [
                        {
                            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory" if "blood" in attr or "chol" in attr else "vital-signs"}]
                        }
                    ],
                    "code": {
                        "coding": [{"system": "http://loinc.org", "code": l_info["code"], "display": l_info["display"]}],
                        "text": l_info["display"]
                    },
                    "subject": {
                        "reference": f"Patient/{patient_ref_id}",
                        "display": user.full_name
                    },
                    "effectiveDateTime": event_iso,
                    "valueQuantity": {
                        "value": float(val),
                        "unit": l_info["unit"],
                        "system": "http://unitsofmeasure.org"
                    }
                }
                entries.append({"fullUrl": f"urn:uuid:{uuid.uuid4()}", "resource": obs_res})
                
    bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        },
        "type": "collection",
        "total": len(entries),
        "entry": entries
    }
    return bundle

def import_fhir_bundle(bundle_data: Dict[str, Any], user: User, db: Session) -> Dict[str, Any]:
    """
    Parses an incoming HL7 FHIR Bundle and synchronizes Patient, Conditions, Observations, and Medications.
    """
    if bundle_data.get("resourceType") != "Bundle":
        raise ValueError("Invalid FHIR payload: root resource must be a 'Bundle'.")
        
    entries = bundle_data.get("entry", [])
    records_added = 0
    profile_updated = False
    details = []
    
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    if not profile:
        profile = HealthProfile(user_id=user.id)
        db.add(profile)
        db.flush()
        
    def _get_list(field):
        if isinstance(field, list):
            return field
        if isinstance(field, str):
            try:
                return json.loads(field)
            except Exception:
                return [s.strip() for s in field.split(",") if s.strip()]
        return []
        
    current_conditions = set(_get_list(profile.chronic_conditions))
    current_meds = _get_list(profile.current_medications)
    
    for entry in entries:
        res = entry.get("resource", {})
        res_type = res.get("resourceType")
        
        # 1. Parse Patient
        if res_type == "Patient":
            if "gender" in res:
                profile.gender = res["gender"].lower()
                profile_updated = True
                details.append(f"Updated gender to {res['gender']}.")
            for ext in res.get("extension", []):
                if "blood-group" in ext.get("url", ""):
                    profile.blood_group = ext.get("valueString", "O+")
                    profile_updated = True
                    details.append(f"Updated blood group to {profile.blood_group}.")
                    
        # 2. Parse Condition
        elif res_type == "Condition":
            code_text = res.get("code", {}).get("text")
            if not code_text and res.get("code", {}).get("coding"):
                code_text = res["code"]["coding"][0].get("display", "Chronic Condition")
            if code_text and code_text not in current_conditions:
                current_conditions.add(code_text)
                profile_updated = True
                details.append(f"Imported condition: {code_text}")
                
        # 3. Parse MedicationStatement
        elif res_type == "MedicationStatement":
            med_text = res.get("medicationCodeableConcept", {}).get("text", "Prescribed Medication")
            dosage = ""
            if res.get("dosage"):
                dosage = res["dosage"][0].get("text", "")
            current_meds.append({"name": med_text, "dose": dosage, "frequency": "Daily"})
            profile_updated = True
            details.append(f"Imported medication: {med_text}")
            
        # 4. Parse Observation
        elif res_type == "Observation":
            code_val = None
            for c in res.get("code", {}).get("coding", []):
                code_val = c.get("code")
                if code_val:
                    break
            val_qty = res.get("valueQuantity", {}).get("value")
            
            if val_qty is not None:
                new_rec = HealthRecord(
                    user_id=user.id,
                    record_type="lab_result",
                    title=res.get("code", {}).get("text", "Imported FHIR Observation"),
                    notes="Imported via HL7 FHIR standard exchange."
                )
                
                # Match LOINC
                if code_val == "8480-6":
                    new_rec.systolic_bp = int(val_qty)
                elif code_val == "8462-4":
                    new_rec.diastolic_bp = int(val_qty)
                elif code_val in ["1558-6", "1521-4"]:
                    new_rec.blood_sugar_fasting = float(val_qty)
                elif code_val == "2093-3":
                    new_rec.total_cholesterol = float(val_qty)
                elif code_val == "718-7":
                    new_rec.hemoglobin = float(val_qty)
                elif code_val == "2708-6":
                    new_rec.spo2 = float(val_qty)
                elif code_val == "8867-4":
                    new_rec.heart_rate = int(val_qty)
                    
                db.add(new_rec)
                records_added += 1
                details.append(f"Imported Observation record: {new_rec.title} ({val_qty})")
                
    if profile_updated:
        profile.chronic_conditions = json.dumps(list(current_conditions))
        profile.current_medications = json.dumps(current_meds)
        
    db.commit()
    
    return {
        "status": "success",
        "records_imported": records_added,
        "profile_updated": profile_updated,
        "details": details
    }

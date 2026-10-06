from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.profile import HealthProfile
from ..schemas.auth import UserRegister, UserLogin, Token, UserOut, ConsentUpdate
from ..services.auth_service import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
        
    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=user_in.email.lower(),
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
        consent_given=user_in.consent_given,
        consent_timestamp=datetime.utcnow()
    )
    db.add(user)
    db.flush()
    
    # Initialize blank health profile
    profile = HealthProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)
    
    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role
    )

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated.")
        
    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role
    )

@router.get("/me", response_model=UserOut)
def get_current_user_profile(user: User = Depends(get_current_user)):
    return user

@router.post("/consent", response_model=UserOut)
def update_consent(consent_in: ConsentUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.consent_given = consent_in.consent_given
    user.consent_timestamp = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

@router.delete("/delete-my-data", status_code=status.HTTP_200_OK)
def delete_my_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    HIPAA / GDPR compliant complete purge of user account, EHR profiles, records, and predictions.
    """
    db.delete(user)
    db.commit()
    return {"status": "success", "message": "All personal health data and account details have been permanently erased."}

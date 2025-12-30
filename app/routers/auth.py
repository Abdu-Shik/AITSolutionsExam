from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.passenger_profile import PassengerProfileCreate, PassengerProfileResponse
from app.models.user import User
from app.models.passenger_profile import PassengerProfile
from app.services.auth_service import create_user, authenticate_user, create_token_for_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (passenger or staff)"""
    if user_data.role not in ["passenger", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'passenger' or 'staff'"
        )
    return create_user(db, user_data)


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = authenticate_user(db, login_data)
    access_token = create_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/profile", response_model=PassengerProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: PassengerProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update passenger profile (passengers only)"""
    if current_user.role != "passenger":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only passengers can create profiles"
        )
    
    existing_profile = db.query(PassengerProfile).filter(
        PassengerProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        # Update existing profile
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(existing_profile, key, value)
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    
    # Create new profile
    profile = PassengerProfile(
        user_id=current_user.id,
        **profile_data.dict()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profile", response_model=PassengerProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get passenger profile"""
    if current_user.role != "passenger":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only passengers have profiles"
        )
    
    profile = db.query(PassengerProfile).filter(
        PassengerProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first."
        )
    
    return profile


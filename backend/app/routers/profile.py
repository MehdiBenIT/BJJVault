from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.athlete_profile import AthleteProfile
from app.models.user import User
from app.schemas.athlete_profile import ALLOWED_BELTS, AthleteProfileCreate, AthleteProfileOut, AthleteProfileUpdate
from app.schemas.user import UserOut

router = APIRouter(tags=["profile"])


@router.get("/users/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=AthleteProfileOut)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(AthleteProfile).filter(AthleteProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not created yet")
    return profile


def _validate_belt(belt: str):
    if belt not in ALLOWED_BELTS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"belt must be one of {ALLOWED_BELTS}")


@router.put("/profile", response_model=AthleteProfileOut)
def upsert_profile(
    payload: AthleteProfileCreate | AthleteProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _validate_belt(payload.belt)

    profile = db.query(AthleteProfile).filter(AthleteProfile.user_id == current_user.id).first()
    if profile:
        for field, value in payload.model_dump().items():
            setattr(profile, field, value)
    else:
        profile = AthleteProfile(user_id=current_user.id, **payload.model_dump())
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile

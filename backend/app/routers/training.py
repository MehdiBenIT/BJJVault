from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.training_entry import TrainingEntry
from app.models.user import User
from app.schemas.training_entry import TrainingEntryCreate, TrainingEntryOut

router = APIRouter(prefix="/training-entries", tags=["training"])


@router.get("", response_model=list[TrainingEntryOut])
def list_entries(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(TrainingEntry)
        .filter(TrainingEntry.user_id == current_user.id)
        .order_by(TrainingEntry.session_date.desc())
        .all()
    )


@router.post("", response_model=TrainingEntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: TrainingEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = TrainingEntry(user_id=current_user.id, **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.query(TrainingEntry).filter(TrainingEntry.id == entry_id, TrainingEntry.user_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training entry not found")
    db.delete(entry)
    db.commit()

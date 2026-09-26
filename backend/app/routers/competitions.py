from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.competition_entry import CompetitionEntry
from app.models.user import User
from app.schemas.competition_entry import CompetitionEntryCreate, CompetitionEntryOut

router = APIRouter(prefix="/competition-entries", tags=["competitions"])


@router.get("", response_model=list[CompetitionEntryOut])
def list_entries(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(CompetitionEntry)
        .filter(CompetitionEntry.user_id == current_user.id)
        .order_by(CompetitionEntry.event_date.desc())
        .all()
    )


@router.post("", response_model=CompetitionEntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(
    payload: CompetitionEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = CompetitionEntry(user_id=current_user.id, **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = (
        db.query(CompetitionEntry)
        .filter(CompetitionEntry.id == entry_id, CompetitionEntry.user_id == current_user.id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition entry not found")
    db.delete(entry)
    db.commit()

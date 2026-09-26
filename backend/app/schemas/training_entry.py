from datetime import date

from pydantic import BaseModel, ConfigDict


class TrainingEntryBase(BaseModel):
    session_date: date
    is_gi: bool = True
    techniques_practiced: str | None = None
    notes: str | None = None


class TrainingEntryCreate(TrainingEntryBase):
    pass


class TrainingEntryOut(TrainingEntryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str

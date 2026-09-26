from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CompetitionEntryBase(BaseModel):
    event_date: date
    tournament: str
    opponent: str | None = None
    result: str = Field(pattern="^(win|loss|draw)$")
    video_link: str | None = None
    notes: str | None = None


class CompetitionEntryCreate(CompetitionEntryBase):
    pass


class CompetitionEntryOut(CompetitionEntryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str

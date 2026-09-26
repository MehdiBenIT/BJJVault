from pydantic import BaseModel, ConfigDict, Field

from app.models.athlete_profile import BELTS


class AthleteProfileBase(BaseModel):
    name: str
    belt: str = Field(default="white")
    weight_class: str | None = None
    academy: str | None = None
    country: str | None = None


class AthleteProfileCreate(AthleteProfileBase):
    pass


class AthleteProfileUpdate(AthleteProfileBase):
    pass


class AthleteProfileOut(AthleteProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str


ALLOWED_BELTS = BELTS

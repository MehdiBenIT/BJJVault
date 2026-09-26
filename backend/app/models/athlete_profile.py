from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

BELTS = ("white", "blue", "purple", "brown", "black")


class AthleteProfile(Base):
    __tablename__ = "athlete_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    belt: Mapped[str] = mapped_column(String(20), nullable=False, default="white")
    weight_class: Mapped[str] = mapped_column(String(50), nullable=True)
    academy: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="athlete_profile")

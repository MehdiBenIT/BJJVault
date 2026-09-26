from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

RESULTS = ("win", "loss", "draw")


class CompetitionEntry(Base):
    __tablename__ = "competition_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    tournament: Mapped[str] = mapped_column(String(255), nullable=False)
    opponent: Mapped[str] = mapped_column(String(255), nullable=True)
    result: Mapped[str] = mapped_column(String(10), nullable=False)
    video_link: Mapped[str] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="competition_entries")

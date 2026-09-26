from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TrainingEntry(Base):
    __tablename__ = "training_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_gi: Mapped[bool] = mapped_column(Boolean, default=True)
    techniques_practiced: Mapped[str] = mapped_column(Text, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="training_entries")

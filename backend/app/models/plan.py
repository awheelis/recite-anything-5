from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Integer, Enum, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PlanStatus(str, enum.Enum):
    active = "active"
    retention_100_day = "retention_100_day"
    weekly_slot = "weekly_slot"
    kissed_goodbye = "kissed_goodbye"
    paused = "paused"


class WeekDay(str, enum.Enum):
    Mon = "Mon"
    Tue = "Tue"
    Wed = "Wed"
    Thu = "Thu"
    Fri = "Fri"
    Sat = "Sat"
    Sun = "Sun"


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    book: Mapped[str] = mapped_column(String, nullable=False)
    translation: Mapped[str] = mapped_column(String, nullable=False, default="KJV")
    total_verses: Mapped[int] = mapped_column(Integer, nullable=False)
    verses_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    days_per_week: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus), nullable=False, default=PlanStatus.active)
    weekly_slot_day: Mapped[Optional[WeekDay]] = mapped_column(Enum(WeekDay), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="plans")
    progress: Mapped["Progress"] = relationship(back_populates="plan", uselist=False, cascade="all, delete-orphan")
    session_logs: Mapped[list["SessionLog"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

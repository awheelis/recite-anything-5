from __future__ import annotations

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import String, Date, Enum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SessionType(str, enum.Enum):
    daily = "daily"
    weeding = "weeding"
    retention = "retention"
    weekly_slot = "weekly_slot"


class SessionLog(Base):
    __tablename__ = "session_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    session_type: Mapped[SessionType] = mapped_column(Enum(SessionType), nullable=False)
    phases_completed: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    completed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    plan: Mapped["Plan"] = relationship(back_populates="session_logs")

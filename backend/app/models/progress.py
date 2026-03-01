from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id"), unique=True, nullable=False, index=True)
    current_verse_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_session_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)
    consecutive_retention_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_weed_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)

    plan: Mapped["Plan"] = relationship(back_populates="progress")

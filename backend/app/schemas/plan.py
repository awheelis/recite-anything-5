from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    book: str
    translation: str = "KJV"
    verses_per_day: int = Field(ge=1)
    days_per_week: int = Field(ge=1, le=7, default=6)
    start_date: date


class WeekEntry(BaseModel):
    week: int
    new_verses_start: str
    new_verses_end: str


class PlanResponse(BaseModel):
    id: str
    book: str
    translation: str
    total_verses: int
    verses_per_day: int
    days_per_week: int
    start_date: date
    target_date: date
    status: str
    weekly_slot_day: Optional[str] = None

    model_config = {"from_attributes": True}

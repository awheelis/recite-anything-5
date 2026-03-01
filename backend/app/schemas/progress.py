from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProgressResponse(BaseModel):
    id: str
    plan_id: str
    current_verse_index: int
    last_session_date: Optional[date] = None
    consecutive_retention_days: int = 0
    last_weed_date: Optional[date] = None

    model_config = {"from_attributes": True}

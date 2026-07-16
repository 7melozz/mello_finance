from __future__ import annotations
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., example="Maria Silva")
    telegram_id: int = Field(..., example=123456789)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Maria Souza")


class UserResponse(BaseModel):
    user_id: int
    name: str
    telegram_id: int
    created_at: date

    model_config = {"from_attributes": True}

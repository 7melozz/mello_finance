from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal, validator


class GoalCreate(BaseModel):
    user_id: int = Field(..., example=1)
    title: str = Field(..., example="Viagem de fim de ano")
    target_amount: condecimal(gt=0) = Field(..., example="5000.00")
    current_amount: condecimal(ge=0) = Field(default=0, example="1250.00")
    goal_type: str = Field(default="saving", example="saving")
    deadline: Optional[date] = Field(None, example="2026-12-31")

    @validator("title")
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title não pode estar vazio")
        return value.strip()

    @validator("goal_type")
    def validate_goal_type(cls, value: str) -> str:
        if value not in {"saving", "spending", "investment"}:
            raise ValueError("goal_type deve ser 'saving', 'spending' ou 'investment'")
        return value


class GoalUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Nova meta")
    target_amount: Optional[condecimal(gt=0)] = Field(None, example="7000.00")
    current_amount: Optional[condecimal(ge=0)] = Field(None, example="3000.00")
    goal_type: Optional[str] = Field(None, example="saving")
    deadline: Optional[date] = Field(None, example="2026-12-31")

    @validator("title")
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("title não pode estar vazio")
        return value.strip() if value is not None else value

    @validator("goal_type")
    def validate_goal_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in {"saving", "spending", "investment"}:
            raise ValueError("goal_type deve ser 'saving', 'spending' ou 'investment'")
        return value


class GoalContribution(BaseModel):
    amount: condecimal(gt=0) = Field(..., example="250.00")


class GoalResponse(BaseModel):
    goal_id: int
    user_id: int
    title: str
    target_amount: Decimal
    current_amount: Decimal
    goal_type: str
    deadline: Optional[date] = None
    status: str
    progress_percentage: float
    remaining_amount: Decimal

    model_config = {"from_attributes": True}


class GoalProgressResponse(BaseModel):
    goal_id: int
    status: str
    progress_percentage: float
    remaining_amount: Decimal
    current_amount: Decimal
    target_amount: Decimal

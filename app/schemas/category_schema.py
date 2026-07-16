from __future__ import annotations
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., example="Alimentação")


class CategoryResponse(BaseModel):
    category_id: int
    name: str

    model_config = {"from_attributes": True}

from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    user_id: int = Field(..., example=1)
    account_type: str = Field(..., example="Conta corrente")
    bank_name: str = Field(..., example="Banco Exemplo")


class AccountUpdate(BaseModel):
    account_type: Optional[str] = Field(None, example="Conta salário")
    bank_name: Optional[str] = Field(None, example="Banco Atualizado")


class AccountResponse(BaseModel):
    account_id: int
    user_id: int
    account_type: str
    bank_name: str

    model_config = {"from_attributes": True}

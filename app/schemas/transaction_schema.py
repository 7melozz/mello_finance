from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal, validator


class TransactionCreate(BaseModel):
    user_id: int = Field(..., example=1)
    account_id: int = Field(..., example=1)
    category_id: int = Field(..., example=1)
    description: str = Field(..., example="Compra no supermercado")
    amount: condecimal(gt=0) = Field(..., example="120.50")
    transaction_type: str = Field(..., example="expense")

    @validator("transaction_type")
    def validate_transaction_type(cls, value: str) -> str:
        if value not in {"expense", "income"}:
            raise ValueError("transaction_type deve ser 'expense' ou 'income'")
        return value


class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, example="Compra supermercado atualizada")
    amount: Optional[condecimal(gt=0)] = Field(None, example="100.00")
    category_id: Optional[int] = Field(None, example=2)


class TransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    account_id: int
    category_id: int
    description: str
    amount: Decimal
    transaction_type: str
    transaction_date: date

    model_config = {"from_attributes": True}

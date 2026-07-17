from __future__ import annotations
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    user_id: int
    period: str
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    largest_expense_category: Optional[str]
    transaction_count: int
    insights: List[str]

    model_config = {"from_attributes": True}

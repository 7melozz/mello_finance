from decimal import Decimal
from typing import Iterable


def calculate_income(transactions: Iterable[dict]) -> Decimal:
    total = Decimal("0")
    for tx in transactions:
        if tx["transaction_type"] == "income":
            total += Decimal(tx["amount"])
    return total


def calculate_expenses(transactions: Iterable[dict]) -> Decimal:
    total = Decimal("0")
    for tx in transactions:
        if tx["transaction_type"] == "expense":
            total += Decimal(tx["amount"])
    return total


def calculate_balance(income: Decimal, expenses: Decimal) -> Decimal:
    return income - expenses


def calculate_transaction_count(transactions: Iterable[dict]) -> int:
    return len(list(transactions))


def find_largest_category(categories: Iterable[dict]) -> str | None:
    if not categories:
        return None
    sorted_categories = sorted(categories, key=lambda item: Decimal(item["total_expense"]), reverse=True)
    return sorted_categories[0]["category_name"]

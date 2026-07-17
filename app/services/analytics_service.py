from datetime import datetime
from decimal import Decimal

from app.analytics.insights import generate_financial_insights
from app.analytics.metrics import (
    calculate_balance,
    calculate_expenses,
    calculate_income,
    calculate_transaction_count,
    find_largest_category,
)
from app.analytics.summaries import format_period
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.user_repository import UserRepository
from app.exceptions import NotFoundError


class AnalyticsService:
    @staticmethod
    def get_financial_summary(user_id: int) -> dict:
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")

        today = datetime.today()
        month = today.month
        year = today.year

        transactions = AnalyticsRepository.get_month_transactions(user_id=user_id, month=month, year=year)
        previous_month = month - 1
        previous_year = year
        if previous_month == 0:
            previous_month = 12
            previous_year -= 1

        previous_expense_rows = AnalyticsRepository.get_previous_month_expenses(user_id=user_id, month=previous_month, year=previous_year)
        previous_month_expenses = sum(Decimal(row["amount"]) for row in previous_expense_rows)

        category_rows = AnalyticsRepository.get_category_expenses(user_id=user_id, month=month, year=year)
        largest_category = find_largest_category(category_rows)

        total_income = calculate_income(transactions)
        total_expenses = calculate_expenses(transactions)
        balance = calculate_balance(total_income, total_expenses)
        transaction_count = calculate_transaction_count(transactions)

        summary = {
            "user_id": user_id,
            "period": format_period(year, month),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "largest_expense_category": largest_category,
            "transaction_count": transaction_count,
            "previous_month_expenses": previous_month_expenses,
        }

        summary["insights"] = generate_financial_insights(summary)
        return summary

from sqlalchemy import text
from app.db.conn import engine


class AnalyticsRepository:
    @staticmethod
    def get_month_transactions(user_id: int, month: int, year: int):
        with engine.connect() as conn:
            query = text(
                "SELECT transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date FROM transactions WHERE user_id = :user_id AND EXTRACT(YEAR FROM transaction_date) = :year AND EXTRACT(MONTH FROM transaction_date) = :month"
            )
            result = conn.execute(query, {"user_id": user_id, "month": month, "year": year})
            return [row for row in result.mappings()]

    @staticmethod
    def get_previous_month_expenses(user_id: int, month: int, year: int):
        with engine.connect() as conn:
            query = text(
                "SELECT amount, transaction_type FROM transactions WHERE user_id = :user_id AND transaction_type = 'expense' AND EXTRACT(YEAR FROM transaction_date) = :year AND EXTRACT(MONTH FROM transaction_date) = :month"
            )
            result = conn.execute(query, {"user_id": user_id, "month": month, "year": year})
            return [row for row in result.mappings()]

    @staticmethod
    def get_category_expenses(user_id: int, month: int, year: int):
        with engine.connect() as conn:
            query = text(
                "SELECT c.name AS category_name, SUM(t.amount) AS total_expense FROM transactions t JOIN categories c ON t.category_id = c.category_id WHERE t.user_id = :user_id AND t.transaction_type = 'expense' AND EXTRACT(YEAR FROM t.transaction_date) = :year AND EXTRACT(MONTH FROM t.transaction_date) = :month GROUP BY c.name ORDER BY total_expense DESC"
            )
            result = conn.execute(query, {"user_id": user_id, "month": month, "year": year})
            return [row for row in result.mappings()]


from sqlalchemy import text
from app.db.conn import engine


class TransactionRepository:
    @staticmethod
    def create_transaction(user_id: int, account_id: int, category_id: int, description: str, amount, transaction_type: str, transaction_date):
        with engine.connect() as conn:
            query = text(
                """
                INSERT INTO transactions (user_id, account_id, category_id, description, amount, transaction_type, transaction_date)
                VALUES (:user_id, :account_id, :category_id, :description, :amount, :transaction_type, :transaction_date)
                RETURNING transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date
                """
            )
            result = conn.execute(
                query,
                {
                    "user_id": user_id,
                    "account_id": account_id,
                    "category_id": category_id,
                    "description": description,
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "transaction_date": transaction_date,
                },
            )
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def get_transaction(transaction_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date FROM transactions WHERE transaction_id = :transaction_id"
            )
            result = conn.execute(query, {"transaction_id": transaction_id})
            return result.mappings().first()

    @staticmethod
    def list_user_transactions(user_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date FROM transactions WHERE user_id = :user_id ORDER BY transaction_date DESC"
            )
            result = conn.execute(query, {"user_id": user_id})
            return [row for row in result.mappings()]

    @staticmethod
    def list_account_transactions(account_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date FROM transactions WHERE account_id = :account_id ORDER BY transaction_date DESC"
            )
            result = conn.execute(query, {"account_id": account_id})
            return [row for row in result.mappings()]

    @staticmethod
    def list_user_month_transactions(user_id: int, year: int, month: int):
        with engine.connect() as conn:
            query = text(
                "SELECT transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date FROM transactions WHERE user_id = :user_id AND EXTRACT(YEAR FROM transaction_date) = :year AND EXTRACT(MONTH FROM transaction_date) = :month ORDER BY transaction_date DESC"
            )
            result = conn.execute(query, {"user_id": user_id, "year": year, "month": month})
            return [row for row in result.mappings()]

    @staticmethod
    def update_transaction(transaction_id: int, description: str | None, amount, category_id: int | None):
        fields = []
        params = {"transaction_id": transaction_id}
        if description is not None:
            fields.append("description = :description")
            params["description"] = description
        if amount is not None:
            fields.append("amount = :amount")
            params["amount"] = amount
        if category_id is not None:
            fields.append("category_id = :category_id")
            params["category_id"] = category_id
        if not fields:
            return None
        with engine.connect() as conn:
            query = text(f"UPDATE transactions SET {', '.join(fields)} WHERE transaction_id = :transaction_id RETURNING transaction_id, user_id, account_id, category_id, description, amount, transaction_type, transaction_date")
            result = conn.execute(query, params)
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def delete_transaction(transaction_id: int):
        with engine.connect() as conn:
            query = text("DELETE FROM transactions WHERE transaction_id = :transaction_id")
            conn.execute(query, {"transaction_id": transaction_id})
            conn.commit()

    @staticmethod
    def category_exists(category_id: int):
        with engine.connect() as conn:
            query = text("SELECT 1 FROM categories WHERE category_id = :category_id")
            result = conn.execute(query, {"category_id": category_id})
            return result.first() is not None

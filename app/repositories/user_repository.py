from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.conn import engine


class UserRepository:
    @staticmethod
    def create_user(name: str, telegram_id: int):
        try:
            with engine.connect() as conn:
                query = text(
                    """
                    INSERT INTO users (name, telegram_id)
                    VALUES (:name, :telegram_id)
                    RETURNING user_id, name, telegram_id, created_at::date AS created_at
                    """
                )
                result = conn.execute(query, {"name": name, "telegram_id": telegram_id})
                conn.commit()
                return result.mappings().first()
        except SQLAlchemyError as exc:
            raise

    @staticmethod
    def get_user(user_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT user_id, name, telegram_id, created_at::date AS created_at FROM users WHERE user_id = :user_id"
            )
            result = conn.execute(query, {"user_id": user_id})
            return result.mappings().first()

    @staticmethod
    def list_users():
        with engine.connect() as conn:
            query = text(
                "SELECT user_id, name, telegram_id, created_at::date AS created_at FROM users ORDER BY user_id"
            )
            result = conn.execute(query)
            return [row for row in result.mappings()]

    @staticmethod
    def update_user(user_id: int, name: str):
        with engine.connect() as conn:
            query = text(
                "UPDATE users SET name = :name WHERE user_id = :user_id RETURNING user_id, name, telegram_id, created_at::date AS created_at"
            )
            result = conn.execute(query, {"user_id": user_id, "name": name})
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def delete_user(user_id: int):
        with engine.connect() as conn:
            query = text("DELETE FROM users WHERE user_id = :user_id")
            conn.execute(query, {"user_id": user_id})
            conn.commit()

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT user_id, name, telegram_id, created_at::date AS created_at FROM users WHERE telegram_id = :telegram_id"
            )
            result = conn.execute(query, {"telegram_id": telegram_id})
            return result.mappings().first()

    @staticmethod
    def count_user_transactions(user_id: int):
        with engine.connect() as conn:
            query = text(
                "SELECT COUNT(1) FROM transactions WHERE user_id = :user_id"
            )
            result = conn.execute(query, {"user_id": user_id})
            return result.scalar()

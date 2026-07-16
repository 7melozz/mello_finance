from sqlalchemy import text
from app.db.conn import engine


class CategoryRepository:
    @staticmethod
    def list_categories():
        with engine.connect() as conn:
            query = text("SELECT category_id, name FROM categories ORDER BY category_id")
            result = conn.execute(query)
            return [row for row in result.mappings()]

    @staticmethod
    def create_category(name: str):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO categories (name, type) VALUES (:name, 'user') RETURNING category_id, name"
            )
            result = conn.execute(query, {"name": name})
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def get_category(category_id: int):
        with engine.connect() as conn:
            query = text("SELECT category_id, name FROM categories WHERE category_id = :category_id")
            result = conn.execute(query, {"category_id": category_id})
            return result.mappings().first()

    @staticmethod
    def category_exists(category_id: int):
        with engine.connect() as conn:
            query = text("SELECT 1 FROM categories WHERE category_id = :category_id")
            result = conn.execute(query, {"category_id": category_id})
            return result.first() is not None

    @staticmethod
    def update_category(category_id: int, name: str):
        with engine.connect() as conn:
            query = text(
                "UPDATE categories SET name = :name WHERE category_id = :category_id RETURNING category_id, name"
            )
            result = conn.execute(query, {"category_id": category_id, "name": name})
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def delete_category(category_id: int):
        with engine.connect() as conn:
            query = text("DELETE FROM categories WHERE category_id = :category_id")
            conn.execute(query, {"category_id": category_id})
            conn.commit()

    @staticmethod
    def count_category_transactions(category_id: int):
        with engine.connect() as conn:
            query = text("SELECT COUNT(1) FROM transactions WHERE category_id = :category_id")
            result = conn.execute(query, {"category_id": category_id})
            return result.scalar()

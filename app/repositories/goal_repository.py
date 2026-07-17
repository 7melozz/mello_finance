from sqlalchemy import text

from app.db.conn import engine


class GoalRepository:
    @staticmethod
    def _ensure_table_exists():
        with engine.connect() as conn:
            query = text(
                """
                CREATE TABLE IF NOT EXISTS goals (
                    goal_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    title VARCHAR(255) NOT NULL,
                    target_amount NUMERIC(12, 2) NOT NULL CHECK (target_amount > 0),
                    current_amount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (current_amount >= 0),
                    goal_type VARCHAR(50) NOT NULL DEFAULT 'saving',
                    deadline DATE,
                    status VARCHAR(20) NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(query)
            conn.commit()

    @staticmethod
    def create_goal(user_id: int, title: str, target_amount, current_amount, goal_type: str, deadline):
        GoalRepository._ensure_table_exists()
        with engine.connect() as conn:
            query = text(
                """
                INSERT INTO goals (user_id, title, target_amount, current_amount, goal_type, deadline, status)
                VALUES (:user_id, :title, :target_amount, :current_amount, :goal_type, :deadline, :status)
                RETURNING goal_id, user_id, title, target_amount, current_amount, goal_type, deadline, status
                """
            )
            status = "completed" if current_amount >= target_amount else "active"
            result = conn.execute(
                query,
                {
                    "user_id": user_id,
                    "title": title,
                    "target_amount": target_amount,
                    "current_amount": current_amount,
                    "goal_type": goal_type,
                    "deadline": deadline,
                    "status": status,
                },
            )
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def get_goal(goal_id: int):
        GoalRepository._ensure_table_exists()
        with engine.connect() as conn:
            query = text(
                "SELECT goal_id, user_id, title, target_amount, current_amount, goal_type, deadline, status FROM goals WHERE goal_id = :goal_id"
            )
            result = conn.execute(query, {"goal_id": goal_id})
            return result.mappings().first()

    @staticmethod
    def list_user_goals(user_id: int):
        GoalRepository._ensure_table_exists()
        with engine.connect() as conn:
            query = text(
                "SELECT goal_id, user_id, title, target_amount, current_amount, goal_type, deadline, status FROM goals WHERE user_id = :user_id ORDER BY created_at DESC"
            )
            result = conn.execute(query, {"user_id": user_id})
            return [row for row in result.mappings()]

    @staticmethod
    def update_goal(goal_id: int, title: str | None, target_amount, current_amount, goal_type: str | None, deadline):
        GoalRepository._ensure_table_exists()
        fields = []
        params = {"goal_id": goal_id}
        if title is not None:
            fields.append("title = :title")
            params["title"] = title
        if target_amount is not None:
            fields.append("target_amount = :target_amount")
            params["target_amount"] = target_amount
        if current_amount is not None:
            fields.append("current_amount = :current_amount")
            params["current_amount"] = current_amount
        if goal_type is not None:
            fields.append("goal_type = :goal_type")
            params["goal_type"] = goal_type
        if deadline is not None:
            fields.append("deadline = :deadline")
            params["deadline"] = deadline
        if not fields:
            return None
        fields.append("status = CASE WHEN current_amount >= target_amount THEN 'completed' ELSE 'active' END")
        with engine.connect() as conn:
            query = text(
                f"UPDATE goals SET {', '.join(fields)} WHERE goal_id = :goal_id RETURNING goal_id, user_id, title, target_amount, current_amount, goal_type, deadline, status"
            )
            result = conn.execute(query, params)
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def contribute_to_goal(goal_id: int, amount):
        GoalRepository._ensure_table_exists()
        with engine.connect() as conn:
            query = text(
                """
                UPDATE goals
                SET current_amount = LEAST(target_amount, current_amount + :amount),
                    status = CASE WHEN current_amount + :amount >= target_amount THEN 'completed' ELSE 'active' END
                WHERE goal_id = :goal_id
                RETURNING goal_id, user_id, title, target_amount, current_amount, goal_type, deadline, status
                """
            )
            result = conn.execute(query, {"goal_id": goal_id, "amount": amount})
            conn.commit()
            return result.mappings().first()

    @staticmethod
    def delete_goal(goal_id: int):
        GoalRepository._ensure_table_exists()
        with engine.connect() as conn:
            query = text("DELETE FROM goals WHERE goal_id = :goal_id")
            conn.execute(query, {"goal_id": goal_id})
            conn.commit()

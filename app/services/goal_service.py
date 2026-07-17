from decimal import Decimal

from app.exceptions import BadRequestError, NotFoundError
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository


class GoalService:
    @staticmethod
    def _serialize_goal(goal):
        if not goal:
            return None
        target_amount = Decimal(str(goal["target_amount"]))
        current_amount = Decimal(str(goal["current_amount"]))
        status = "completed" if current_amount >= target_amount else "active"
        progress_percentage = 100.0 if target_amount <= 0 else round(float(min(current_amount / target_amount * 100, 100.0)), 2)
        remaining_amount = max(target_amount - current_amount, Decimal("0.00"))
        return {
            **goal,
            "status": status,
            "progress_percentage": progress_percentage,
            "remaining_amount": remaining_amount,
        }

    @staticmethod
    def create_goal(user_id: int, title: str, target_amount: Decimal, current_amount: Decimal, goal_type: str, deadline):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        if not title.strip():
            raise BadRequestError("title não pode estar vazio")
        if target_amount <= 0:
            raise BadRequestError("target_amount deve ser maior que zero")
        if current_amount < 0:
            raise BadRequestError("current_amount não pode ser negativo")
        if goal_type not in {"saving", "spending", "investment"}:
            raise BadRequestError("goal_type deve ser 'saving', 'spending' ou 'investment'")

        created = GoalRepository.create_goal(
            user_id=user_id,
            title=title.strip(),
            target_amount=target_amount,
            current_amount=min(current_amount, target_amount),
            goal_type=goal_type,
            deadline=deadline,
        )
        return GoalService._serialize_goal(created)

    @staticmethod
    def get_goal(goal_id: int):
        goal = GoalRepository.get_goal(goal_id)
        if not goal:
            raise NotFoundError("Meta não encontrada")
        return GoalService._serialize_goal(goal)

    @staticmethod
    def list_user_goals(user_id: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        goals = GoalRepository.list_user_goals(user_id)
        return [GoalService._serialize_goal(goal) for goal in goals]

    @staticmethod
    def update_goal(goal_id: int, title: str | None, target_amount: Decimal | None, current_amount: Decimal | None, goal_type: str | None, deadline):
        goal = GoalRepository.get_goal(goal_id)
        if not goal:
            raise NotFoundError("Meta não encontrada")
        if title is not None and not title.strip():
            raise BadRequestError("title não pode estar vazio")
        if target_amount is not None and target_amount <= 0:
            raise BadRequestError("target_amount deve ser maior que zero")
        if current_amount is not None and current_amount < 0:
            raise BadRequestError("current_amount não pode ser negativo")
        if goal_type is not None and goal_type not in {"saving", "spending", "investment"}:
            raise BadRequestError("goal_type deve ser 'saving', 'spending' ou 'investment'")

        normalized_target = target_amount if target_amount is not None else Decimal(str(goal["target_amount"]))
        normalized_current = current_amount if current_amount is not None else Decimal(str(goal["current_amount"]))
        if normalized_current > normalized_target:
            normalized_current = normalized_target

        updated = GoalRepository.update_goal(
            goal_id=goal_id,
            title=title.strip() if title is not None else None,
            target_amount=normalized_target,
            current_amount=normalized_current,
            goal_type=goal_type,
            deadline=deadline,
        )
        return GoalService._serialize_goal(updated)

    @staticmethod
    def contribute_to_goal(goal_id: int, amount: Decimal):
        goal = GoalRepository.get_goal(goal_id)
        if not goal:
            raise NotFoundError("Meta não encontrada")
        if amount <= 0:
            raise BadRequestError("amount deve ser maior que zero")

        updated = GoalRepository.contribute_to_goal(goal_id, amount)
        return GoalService._serialize_goal(updated)

    @staticmethod
    def get_goal_progress(goal_id: int):
        goal = GoalRepository.get_goal(goal_id)
        if not goal:
            raise NotFoundError("Meta não encontrada")
        return GoalService._serialize_goal(goal)

    @staticmethod
    def delete_goal(goal_id: int):
        goal = GoalRepository.get_goal(goal_id)
        if not goal:
            raise NotFoundError("Meta não encontrada")
        GoalRepository.delete_goal(goal_id)

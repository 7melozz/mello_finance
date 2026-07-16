from app.exceptions import BadRequestError, ConflictError, NotFoundError
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def create_user(name: str, telegram_id: int):
        existing = UserRepository.get_user_by_telegram_id(telegram_id)
        if existing:
            raise ConflictError("telegram_id já cadastrado")
        return UserRepository.create_user(name=name, telegram_id=telegram_id)

    @staticmethod
    def get_user(user_id: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        return user

    @staticmethod
    def list_users():
        return UserRepository.list_users()

    @staticmethod
    def update_user(user_id: int, name: str):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        if not name.strip():
            raise BadRequestError("name não pode estar vazio")
        return UserRepository.update_user(user_id=user_id, name=name.strip())

    @staticmethod
    def delete_user(user_id: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        transactions = UserRepository.count_user_transactions(user_id)
        if transactions:
            raise ConflictError("Não é possível excluir usuário com transações vinculadas")
        UserRepository.delete_user(user_id)

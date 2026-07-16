from app.exceptions import BadRequestError, NotFoundError
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository


class AccountService:
    @staticmethod
    def create_account(user_id: int, account_name: str, bank_name: str):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        if not account_name.strip():
            raise BadRequestError("account_name não pode estar vazio")
        if not bank_name.strip():
            raise BadRequestError("bank_name não pode estar vazio")
        return AccountRepository.create_account(user_id=user_id, account_name=account_name.strip(), bank_name=bank_name.strip())

    @staticmethod
    def get_account(account_id: int):
        account = AccountRepository.get_account(account_id)
        if not account:
            raise NotFoundError("Conta não encontrada")
        return account

    @staticmethod
    def list_user_accounts(user_id: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        return AccountRepository.list_user_accounts(user_id)

    @staticmethod
    def update_account(account_id: int, account_name: str | None, bank_name: str | None):
        account = AccountRepository.get_account(account_id)
        if not account:
            raise NotFoundError("Conta não encontrada")
        if account_name is not None and not account_name.strip():
            raise BadRequestError("account_name não pode estar vazio")
        if bank_name is not None and not bank_name.strip():
            raise BadRequestError("bank_name não pode estar vazio")
        return AccountRepository.update_account(
            account_id=account_id,
            account_name=account_name.strip() if account_name is not None else None,
            bank_name=bank_name.strip() if bank_name is not None else None,
        )

    @staticmethod
    def delete_account(account_id: int):
        account = AccountRepository.get_account(account_id)
        if not account:
            raise NotFoundError("Conta não encontrada")
        AccountRepository.delete_account(account_id)

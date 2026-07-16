from datetime import date
from decimal import Decimal
from app.exceptions import BadRequestError, NotFoundError
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository


class TransactionService:
    @staticmethod
    def create_transaction(user_id: int, account_id: int, category_id: int, description: str, amount: Decimal, transaction_type: str):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        account = AccountRepository.get_account(account_id)
        if not account:
            raise NotFoundError("Conta não encontrada")
        if account["user_id"] != user_id:
            raise BadRequestError("Conta não pertence ao usuário informado")
        if not CategoryRepository.category_exists(category_id):
            raise NotFoundError("Categoria não encontrada")
        if not description.strip():
            raise BadRequestError("description não pode estar vazio")
        if amount <= 0:
            raise BadRequestError("amount deve ser maior que zero")
        if transaction_type not in {"expense", "income"}:
            raise BadRequestError("transaction_type deve ser 'expense' ou 'income'")

        return TransactionRepository.create_transaction(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            description=description.strip(),
            amount=amount,
            transaction_type=transaction_type,
            transaction_date=date.today(),
        )

    @staticmethod
    def get_transaction(transaction_id: int):
        transaction = TransactionRepository.get_transaction(transaction_id)
        if not transaction:
            raise NotFoundError("Transação não encontrada")
        return transaction

    @staticmethod
    def list_user_transactions(user_id: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        return TransactionRepository.list_user_transactions(user_id)

    @staticmethod
    def list_account_transactions(account_id: int):
        account = AccountRepository.get_account(account_id)
        if not account:
            raise NotFoundError("Conta não encontrada")
        return TransactionRepository.list_account_transactions(account_id)

    @staticmethod
    def list_user_month_transactions(user_id: int, year: int, month: int):
        user = UserRepository.get_user(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        return TransactionRepository.list_user_month_transactions(user_id, year, month)

    @staticmethod
    def update_transaction(transaction_id: int, description: str | None, amount, category_id: int | None):
        transaction = TransactionRepository.get_transaction(transaction_id)
        if not transaction:
            raise NotFoundError("Transação não encontrada")
        if description is not None and not description.strip():
            raise BadRequestError("description não pode estar vazio")
        if amount is not None and amount <= 0:
            raise BadRequestError("amount deve ser maior que zero")
        if category_id is not None and not CategoryRepository.category_exists(category_id):
            raise NotFoundError("Categoria não encontrada")
        return TransactionRepository.update_transaction(
            transaction_id=transaction_id,
            description=description.strip() if description is not None else None,
            amount=amount,
            category_id=category_id,
        )

    @staticmethod
    def delete_transaction(transaction_id: int):
        transaction = TransactionRepository.get_transaction(transaction_id)
        if not transaction:
            raise NotFoundError("Transação não encontrada")
        TransactionRepository.delete_transaction(transaction_id)

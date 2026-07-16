from datetime import date
from decimal import Decimal

from app.funcs import (
    create_account,
    create_reminder,
    create_transaction,
    create_user,
    get_accounts,
    get_reminders,
    get_transactions,
    get_users,
)


def register_user(name, telegram_id):
    """Fluxo completo de cadastro de usuário."""
    users = get_users()

    for user in users:
        if user["telegram_id"] == telegram_id:
            return user["user_id"]

    return create_user(name=name, telegram_id=telegram_id)


def create_default_account(user_id):
    """Cria conta padrão para novo usuário."""
    return create_account(
        user_id=user_id,
        bank_name="Não informado",
        account_type="corrente",
        current_balance=Decimal("0.00"),
    )


def process_transaction(user_id, account_id, description, amount, transaction_type, category_id=1):
    """Processa uma transação completa."""
    if transaction_type not in {"expense", "income"}:
        raise ValueError("Tipo de transação inválido")

    return create_transaction(
        user_id=user_id,
        account_id=account_id,
        category_id=category_id,
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        transaction_date=date.today(),
    )


def process_expense(user_id, account_id, description, amount, category_id=1):
    """Atalho para despesas."""
    return process_transaction(
        user_id=user_id,
        account_id=account_id,
        description=description,
        amount=amount,
        transaction_type="expense",
        category_id=category_id,
    )


def process_income(user_id, account_id, description, amount, category_id=1):
    """Atalho para receitas."""
    return process_transaction(
        user_id=user_id,
        account_id=account_id,
        description=description,
        amount=amount,
        transaction_type="income",
        category_id=category_id,
    )


def get_financial_summary(user_id):
    """Retorna resumo financeiro simples."""
    transactions = get_transactions(user_id)

    total_income = Decimal("0")
    total_expense = Decimal("0")

    for transaction in transactions:
        if transaction["transaction_type"] == "income":
            total_income += transaction["amount"]
        else:
            total_expense += transaction["amount"]

    balance = total_income - total_expense

    return {
        "income": total_income,
        "expense": total_expense,
        "balance": balance,
    }


def create_user_complete(name, telegram_id):
    """Primeiro fluxo real da Mello."""
    user_id = register_user(name, telegram_id)
    accounts = get_accounts(user_id)

    if not accounts:
        account_id = create_default_account(user_id)
    else:
        account_id = accounts[0]["account_id"]

    return {"user_id": user_id, "account_id": account_id}


def add_reminder(user_id, description, due_date):
    return create_reminder(user_id, description, due_date)


def list_user_reminders(user_id):
    return get_reminders(user_id)

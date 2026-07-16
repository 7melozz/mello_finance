from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.conn import engine

"""Funções auxiliares para operações de usuários, transações, contas e lembretes."""


def _validate_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("nome inválido")
    return name.strip()


def _validate_telegram_id(telegram_id):
    if isinstance(telegram_id, str):
        try:
            telegram_id = int(telegram_id)
        except ValueError as exc:
            raise ValueError("telegram_id deve ser um número inteiro.") from exc

    if not isinstance(telegram_id, int):
        raise ValueError("telegram_id deve ser um número inteiro.")
    return telegram_id


def _handle_db_error(exc, context):
    print(exc)
    raise RuntimeError(f"Erro ao {context}") from exc


def create_user(name, telegram_id):
    name = _validate_name(name)
    telegram_id = _validate_telegram_id(telegram_id)

    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO users (name, telegram_id)
                VALUES (:name, :telegram_id)
                RETURNING user_id;
            """)
            result = conn.execute(query, {"name": name, "telegram_id": telegram_id})
            conn.commit()
            return result.scalar()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "criar usuário")


def get_users():
    with engine.connect() as conn:
        query = text("SELECT user_id, name, telegram_id FROM users;")
        result = conn.execute(query)
        return [dict(row) for row in result.mappings()]


def create_transaction(user_id, account_id, category_id, description, amount, transaction_type, transaction_date):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id inválido")
    if not isinstance(category_id, int) or category_id <= 0:
        raise ValueError("category_id inválido")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description inválida")
    if not isinstance(amount, (int, float, Decimal)):
        raise ValueError("amount inválido")
    if isinstance(amount, int):
        amount = Decimal(amount)
    elif isinstance(amount, float):
        amount = Decimal(str(amount))
    else:
        amount = Decimal(str(amount))
    if amount <= 0:
        raise ValueError("amount deve ser maior que zero")
    if transaction_type not in {"expense", "income"}:
        raise ValueError("transaction_type deve ser 'expense' ou 'income'")

    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO transactions (user_id, account_id, category_id, description, amount, transaction_type, transaction_date)
                VALUES (:user_id, :account_id, :category_id, :description, :amount, :transaction_type, :transaction_date)
                RETURNING transaction_id;
            """)
            result = conn.execute(query, {
                "user_id": user_id,
                "account_id": account_id,
                "category_id": category_id,
                "description": description.strip(),
                "amount": amount,
                "transaction_type": transaction_type,
                "transaction_date": transaction_date,
            })
            conn.commit()
            return result.scalar()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "criar transação")


def get_transactions(user_id):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")

    with engine.connect() as conn:
        query = text("SELECT * FROM transactions WHERE user_id = :user_id ORDER BY transaction_date DESC;")
        result = conn.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]


def update_transaction(transaction_id, description=None, amount=None, category_id=None):
    if not isinstance(transaction_id, int) or transaction_id <= 0:
        raise ValueError("transaction_id inválido")

    try:
        with engine.connect() as conn:
            fields = []
            params = {"transaction_id": transaction_id}
            if description is not None:
                if not isinstance(description, str) or not description.strip():
                    raise ValueError("description inválida")
                fields.append("description = :description")
                params["description"] = description.strip()
            if amount is not None:
                if not isinstance(amount, (int, Decimal)):
                    raise ValueError("amount inválido")
                if isinstance(amount, int):
                    amount = Decimal(amount)
                else:
                    amount = Decimal(str(amount))
                if amount <= 0:
                    raise ValueError("amount deve ser maior que zero")
                fields.append("amount = :amount")
                params["amount"] = amount
            if category_id is not None:
                if not isinstance(category_id, int) or category_id <= 0:
                    raise ValueError("category_id inválido")
                fields.append("category_id = :category_id")
                params["category_id"] = category_id

            if not fields:
                raise ValueError("Pelo menos um campo deve ser informado para atualizar a transação.")

            query = text(f"UPDATE transactions SET {', '.join(fields)} WHERE transaction_id = :transaction_id")
            conn.execute(query, params)
            conn.commit()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "atualizar transação")


def delete_transaction(transaction_id):
    if not isinstance(transaction_id, int) or transaction_id <= 0:
        raise ValueError("transaction_id inválido")

    try:
        with engine.connect() as conn:
            query = text("DELETE FROM transactions WHERE transaction_id = :transaction_id")
            conn.execute(query, {"transaction_id": transaction_id})
            conn.commit()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "deletar transação")


def create_account(user_id, bank_name, account_type, current_balance=0):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")
    if not isinstance(bank_name, str) or not bank_name.strip():
        raise ValueError("bank_name inválido")
    if not isinstance(account_type, str) or not account_type.strip():
        raise ValueError("account_type inválido")
    if not isinstance(current_balance, (int, Decimal)):
        raise ValueError("current_balance inválido")
    if isinstance(current_balance, int):
        current_balance = Decimal(current_balance)
    else:
        current_balance = Decimal(str(current_balance))

    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO accounts (user_id, bank_name, account_type, current_balance)
                VALUES (:user_id, :bank_name, :account_type, :current_balance)
                RETURNING account_id;
            """)
            result = conn.execute(query, {
                "user_id": user_id,
                "bank_name": bank_name.strip(),
                "account_type": account_type.strip(),
                "current_balance": current_balance,
            })
            conn.commit()
            return result.scalar()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "criar conta")


def get_accounts(user_id):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")

    with engine.connect() as conn:
        query = text("SELECT * FROM accounts WHERE user_id = :user_id;")
        result = conn.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]


def create_reminder(user_id, description, due_date):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description inválida")

    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO reminders (user_id, description, due_date)
                VALUES (:user_id, :description, :due_date)
                RETURNING reminder_id;
            """)
            result = conn.execute(query, {
                "user_id": user_id,
                "description": description.strip(),
                "due_date": due_date,
            })
            conn.commit()
            return result.scalar()
    except SQLAlchemyError as exc:
        _handle_db_error(exc, "criar lembrete")


def get_reminders(user_id):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")

    with engine.connect() as conn:
        query = text("SELECT * FROM reminders WHERE user_id = :user_id ORDER BY due_date;")
        result = conn.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]


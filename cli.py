import argparse
import sys
from decimal import Decimal
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.legacy.funcs import (
    create_account,
    create_reminder,
    create_transaction,
    create_user,
    get_accounts,
    get_reminders,
    get_transactions,
    get_users,
)


def _parse_decimal(value):
    return Decimal(value)


def _parse_date(value):
    return date.fromisoformat(value)


def build_parser():
    parser = argparse.ArgumentParser(description="CLI simples da Mello")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-users", help="Lista todos os usuários")

    subparsers.add_parser("list-accounts", help="Lista contas de um usuário")
    subparsers.add_parser("list-transactions", help="Lista transações de um usuário")
    subparsers.add_parser("list-reminders", help="Lista lembretes de um usuário")

    create_user_parser = subparsers.add_parser("create-user", help="Cria um usuário")
    create_user_parser.add_argument("name")
    create_user_parser.add_argument("telegram_id", type=int)

    create_account_parser = subparsers.add_parser("create-account", help="Cria uma conta")
    create_account_parser.add_argument("user_id", type=int)
    create_account_parser.add_argument("bank_name")
    create_account_parser.add_argument("account_type")
    create_account_parser.add_argument("current_balance", type=_parse_decimal, nargs="?", default=Decimal("0"))

    create_transaction_parser = subparsers.add_parser("create-transaction", help="Cria uma transação")
    create_transaction_parser.add_argument("user_id", type=int)
    create_transaction_parser.add_argument("account_id", type=int)
    create_transaction_parser.add_argument("category_id", type=int)
    create_transaction_parser.add_argument("description")
    create_transaction_parser.add_argument("amount", type=_parse_decimal)
    create_transaction_parser.add_argument("transaction_type")
    create_transaction_parser.add_argument("transaction_date", type=_parse_date)

    create_reminder_parser = subparsers.add_parser("create-reminder", help="Cria um lembrete")
    create_reminder_parser.add_argument("user_id", type=int)
    create_reminder_parser.add_argument("description")
    create_reminder_parser.add_argument("due_date", type=_parse_date)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "create-user":
            user_id = create_user(args.name, args.telegram_id)
            print(f"Usuário criado com id {user_id}")
            return

        if args.command == "list-users":
            print(get_users())
            return

        if args.command == "create-account":
            account_id = create_account(args.user_id, args.bank_name, args.account_type, args.current_balance)
            print(f"Conta criada com id {account_id}")
            return

        if args.command == "list-accounts":
            print(get_accounts(args.user_id))
            return

        if args.command == "create-transaction":
            transaction_id = create_transaction(
                args.user_id,
                args.account_id,
                args.category_id,
                args.description,
                args.amount,
                args.transaction_type,
                args.transaction_date.isoformat(),
            )
            print(f"Transação criada com id {transaction_id}")
            return

        if args.command == "create-reminder":
            reminder_id = create_reminder(args.user_id, args.description, args.due_date.isoformat())
            print(f"Lembrete criado com id {reminder_id}")
            return

        if args.command == "list-transactions":
            print(get_transactions(args.user_id))
            return

        if args.command == "list-reminders":
            print(get_reminders(args.user_id))
            return
    except (ValueError, RuntimeError) as exc:
        print(f"Erro: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()


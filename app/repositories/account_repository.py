from sqlalchemy import text

from app.db.conn import engine


class AccountRepository:


    @staticmethod
    def create_account(
        user_id: int,
        account_type: str,
        bank_name: str
    ):

        with engine.connect() as conn:

            query = text(
                """
                INSERT INTO accounts
                (
                    user_id,
                    bank_name,
                    account_type,
                    current_balance
                )

                VALUES
                (
                    :user_id,
                    :bank_name,
                    :account_type,
                    :current_balance
                )

                RETURNING
                    account_id,
                    user_id,
                    bank_name,
                    account_type
                """
            )


            result = conn.execute(
                query,
                {
                    "user_id": user_id,
                    "bank_name": bank_name,
                    "account_type": account_type,
                    "current_balance": 0,
                }
            )

            conn.commit()

            return result.mappings().first()



    @staticmethod
    def get_account(account_id: int):

        with engine.connect() as conn:

            query = text(
                """
                SELECT
                    account_id,
                    user_id,
                    bank_name,
                    account_type

                FROM accounts

                WHERE account_id = :account_id
                """
            )

            result = conn.execute(
                query,
                {
                    "account_id": account_id
                }
            )

            return result.mappings().first()



    @staticmethod
    def list_user_accounts(user_id: int):

        with engine.connect() as conn:

            query = text(
                """
                SELECT
                    account_id,
                    user_id,
                    bank_name,
                    account_type

                FROM accounts

                WHERE user_id = :user_id

                ORDER BY account_id
                """
            )

            result = conn.execute(
                query,
                {
                    "user_id": user_id
                }
            )

            return list(result.mappings())



    @staticmethod
    def update_account(
        account_id: int,
        account_type: str | None,
        bank_name: str | None
    ):

        fields = []
        params = {
            "account_id": account_id
        }


        if account_type is not None:

            fields.append(
                "account_type = :account_type"
            )

            params["account_type"] = account_type


        if bank_name is not None:

            fields.append(
                "bank_name = :bank_name"
            )

            params["bank_name"] = bank_name


        if not fields:
            return None


        with engine.connect() as conn:

            query = text(
                f"""
                UPDATE accounts

                SET {', '.join(fields)}

                WHERE account_id = :account_id

                RETURNING
                    account_id,
                    user_id,
                    bank_name,
                    account_type
                """
            )


            result = conn.execute(
                query,
                params
            )

            conn.commit()

            return result.mappings().first()



    @staticmethod
    def delete_account(account_id: int):

        with engine.connect() as conn:

            query = text(
                """
                DELETE FROM accounts
                WHERE account_id = :account_id
                """
            )

            conn.execute(
                query,
                {
                    "account_id": account_id
                }
            )

            conn.commit()



    @staticmethod
    def exists_account(account_id: int):

        with engine.connect() as conn:

            query = text(
                """
                SELECT 1
                FROM accounts
                WHERE account_id = :account_id
                """
            )

            result = conn.execute(
                query,
                {
                    "account_id": account_id
                }
            )

            return result.first() is not None



    @staticmethod
    def get_account_owner(account_id: int):

        with engine.connect() as conn:

            query = text(
                """
                SELECT user_id

                FROM accounts

                WHERE account_id = :account_id
                """
            )

            result = conn.execute(
                query,
                {
                    "account_id": account_id
                }
            )

            row = result.first()

            return row[0] if row else None
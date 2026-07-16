from fastapi import APIRouter

from app.services.mello_service import (
    create_user_complete,
    process_expense
)


router = APIRouter()


@router.post("/users")
def create_user(name: str, telegram_id: int):

    user = create_user_complete(
        name,
        telegram_id
    )

    return user



@router.post("/expense")
def create_expense(
    user_id: int,
    account_id: int,
    description: str,
    amount: float
):

    transaction_id = process_expense(
        user_id=user_id,
        account_id=account_id,
        description=description,
        amount=amount
    )

    return {
        "transaction_id": transaction_id
    }
from fastapi import APIRouter, HTTPException, Query
from app.schemas.transaction_schema import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService
from app.exceptions import BadRequestError, NotFoundError

router = APIRouter(tags=["Transactions"])


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(payload: TransactionCreate):
    try:
        return TransactionService.create_transaction(
            user_id=payload.user_id,
            account_id=payload.account_id,
            category_id=payload.category_id,
            description=payload.description,
            amount=payload.amount,
            transaction_type=payload.transaction_type,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int):
    try:
        return TransactionService.get_transaction(transaction_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/users/{user_id}/transactions", response_model=list[TransactionResponse])
def list_user_transactions(user_id: int):
    try:
        return TransactionService.list_user_transactions(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/users/{user_id}/transactions/month", response_model=list[TransactionResponse])
def list_user_month_transactions(
    user_id: int,
    year: int = Query(..., examples={"year": {"value": 2026}}),
    month: int = Query(..., ge=1, le=12, examples={"month": {"value": 7}}),
):
    try:
        return TransactionService.list_user_month_transactions(user_id=user_id, year=year, month=month)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def list_account_transactions(account_id: int):
    try:
        return TransactionService.list_account_transactions(account_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, payload: TransactionUpdate):
    try:
        return TransactionService.update_transaction(
            transaction_id=transaction_id,
            description=payload.description,
            amount=payload.amount,
            category_id=payload.category_id,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int):
    try:
        TransactionService.delete_transaction(transaction_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

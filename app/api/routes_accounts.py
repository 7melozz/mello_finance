from fastapi import APIRouter, HTTPException
from app.schemas.account_schema import AccountCreate, AccountResponse, AccountUpdate
from app.services.account_service import AccountService
from app.exceptions import BadRequestError, NotFoundError

router = APIRouter(tags=["Accounts"])


@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(payload: AccountCreate):
    try:
        return AccountService.create_account(
            user_id=payload.user_id,
            account_type=payload.account_type,
            bank_name=payload.bank_name,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    try:
        return AccountService.get_account(account_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/users/{user_id}/accounts", response_model=list[AccountResponse])
def list_user_accounts(user_id: int):
    try:
        return AccountService.list_user_accounts(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/accounts/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, payload: AccountUpdate):
    try:
        return AccountService.update_account(
            account_id=account_id,
            account_type=payload.account_type,
            bank_name=payload.bank_name,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/accounts/{account_id}", status_code=204)
def delete_account(account_id: int):
    try:
        AccountService.delete_account(account_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

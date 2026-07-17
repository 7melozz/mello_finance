from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.exceptions import BadRequestError, ConflictError, NotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/telegram/{telegram_id}", response_model=UserResponse)
def get_user_by_telegram(telegram_id: int):
    try:
        return UserService.get_user_by_telegram_id(telegram_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    try:
        return UserService.create_user(name=payload.name, telegram_id=payload.telegram_id)
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    try:
        return UserService.get_user(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("", response_model=list[UserResponse])
def list_users():
    return UserService.list_users()


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate):
    try:
        return UserService.update_user(user_id, payload.name)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    try:
        UserService.delete_user(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@router.get("/telegram/{telegram_id}")
def get_user_by_telegram(telegram_id: int):
    try:
        return UserService.get_user_by_telegram(telegram_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
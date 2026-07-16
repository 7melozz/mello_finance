from fastapi import APIRouter, HTTPException
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService
from app.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories():
    return CategoryService.list_categories()


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(payload: CategoryCreate):
    try:
        return CategoryService.create_category(name=payload.name)
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryCreate):
    try:
        return CategoryService.update_category(category_id=category_id, name=payload.name)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int):
    try:
        CategoryService.delete_category(category_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except BadRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

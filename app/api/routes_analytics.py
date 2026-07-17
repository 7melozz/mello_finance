from fastapi import APIRouter, HTTPException
from app.schemas.analytics_schema import SummaryResponse
from app.services.analytics_service import AnalyticsService
from app.exceptions import NotFoundError

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/summary/{user_id}", response_model=SummaryResponse)
def get_financial_summary(user_id: int):
    try:
        return AnalyticsService.get_financial_summary(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

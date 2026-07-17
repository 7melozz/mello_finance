from fastapi import APIRouter, HTTPException, status

from app.exceptions import BadRequestError, NotFoundError
from app.schemas.goal_schema import (
    GoalContribution,
    GoalCreate,
    GoalProgressResponse,
    GoalResponse,
    GoalUpdate
)
from app.services.goal_service import GoalService


router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


def handle_exception(exc):
    if isinstance(exc, NotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    if isinstance(exc, BadRequestError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED
)
def create_goal(payload: GoalCreate):

    try:
        return GoalService.create_goal(
            user_id=payload.user_id,
            title=payload.title,
            target_amount=payload.target_amount,
            current_amount=payload.current_amount,
            goal_type=payload.goal_type,
            deadline=payload.deadline,
        )

    except (NotFoundError, BadRequestError) as exc:
        handle_exception(exc)



@router.get(
    "/user/{user_id}",
    response_model=list[GoalResponse]
)
def list_user_goals(user_id: int):

    try:
        return GoalService.list_user_goals(user_id)

    except NotFoundError as exc:
        handle_exception(exc)

#@router.get(
 #   "/{goal_id}",
  #  response_model=GoalResponse
#)
#def get_goal(goal_id: int):

 #   try:
  #      return GoalService.get_goal(goal_id)

   # except NotFoundError as exc:
    #    handle_exception(exc)



@router.patch(
    "/{goal_id}",
    response_model=GoalResponse
)
def update_goal(
    goal_id: int,
    payload: GoalUpdate
):

    try:
        return GoalService.update_goal(
            goal_id=goal_id,
            title=payload.title,
            target_amount=payload.target_amount,
            current_amount=payload.current_amount,
            goal_type=payload.goal_type,
            deadline=payload.deadline,
        )

    except (NotFoundError, BadRequestError) as exc:
        handle_exception(exc)



@router.post(
    "/{goal_id}/contribute",
    response_model=GoalResponse
)
def contribute_to_goal(
    goal_id: int,
    payload: GoalContribution
):

    try:
        return GoalService.contribute_to_goal(
            goal_id,
            payload.amount
        )

    except (NotFoundError, BadRequestError) as exc:
        handle_exception(exc)



@router.get(
    "/{goal_id}/progress",
    response_model=GoalProgressResponse
)
def get_goal_progress(goal_id: int):

    try:
        return GoalService.get_goal_progress(goal_id)

    except NotFoundError as exc:
        handle_exception(exc)



@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_goal(goal_id: int):

    try:
        GoalService.delete_goal(goal_id)

    except NotFoundError as exc:
        handle_exception(exc)
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas.mixins import UserIdFilmIdMixinSchema
from schemas.review_schema import (
    ReviewInDBCreate,
    ReviewInDBFull,
    ReviewInDBUpdate,
)
from services.review_service import ReviewService, get_review_service


router = APIRouter()


@router.post(
    "/review",
    response_model=ReviewInDBFull,
    status_code=HTTPStatus.CREATED,
    description="Оставить отзыв на фильм.",
)
async def create_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: ReviewInDBCreate,
) -> ReviewInDBFull:
    """Пользователь ставит лайк фильму."""
    new_review = await review_service.create(db=db, review_data=review_data)
    return new_review


@router.post(
    "/review/show",
    response_model=ReviewInDBFull,
    status_code=HTTPStatus.OK,
    description="Получить отзыв пользователя на фильм.",
)
async def get_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: UserIdFilmIdMixinSchema,
) -> ReviewInDBFull:
    """Получить отзыв пользователя на фильм из БД."""
    review = await review_service.get(db=db, review_data=review_data)
    return review


@router.patch(
    "/review",
    response_model=ReviewInDBFull,
    description="Обновить отзыв.",
    status_code=HTTPStatus.OK,
)
async def update_review(
    db: Annotated[AsyncSession, Depends(get_session)],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    review_data: ReviewInDBUpdate,
) -> ReviewInDBFull:
    """Обновить отзыв пользователя о фильме."""
    result = await review_service.update(db=db, review_data=review_data)
    return result


@router.delete(
    "/review",
    status_code=HTTPStatus.OK,
    description="Удалить отзыв пользователя на фильм.",
)
async def delete_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: UserIdFilmIdMixinSchema,
) -> dict[str, str]:
    """Удалить отзыв пользователя на фильм из БД."""
    await review_service.delete(db=db, review_data=review_data)
    return {"detail": "Отзыв удален."}

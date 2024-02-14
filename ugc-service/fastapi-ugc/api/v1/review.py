from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas.mixins import UserIdFilmIdMixinSchema
from schemas.review_schema import ReviewInDBCreate, RevieInDBFull
from services.review_service import ReviewService, get_review_service


router = APIRouter()


@router.post(
    "/review",
    response_model=RevieInDBFull,
    status_code=HTTPStatus.CREATED,
    description="Оставить отзыв на фильм.",
)
async def create_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: ReviewInDBCreate,
) -> RevieInDBFull:
    """Пользователь ставит лайк фильму."""
    new_review = await review_service.create_like_in_db(
        db=db, review_data=review_data
    )
    return new_review


@router.get(
    "/review",
    response_model=RevieInDBFull,
    status_code=HTTPStatus.OK,
    description="Получить отзыв пользователя на фильм.",
)
async def get_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: UserIdFilmIdMixinSchema,
) -> RevieInDBFull:
    """Получить отзыв пользователя на фильм из БД."""
    review = await review_service.get_review_from_db(
        db=db, review_data=review_data
    )
    return review


@router.delete(
    "/review",
    response_model=RevieInDBFull,
    status_code=HTTPStatus.OK,
    description="Удалить отзыв пользователя на фильм.",
)
async def delete_review(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: UserIdFilmIdMixinSchema,
) -> dict[str, str]:
    """Удалить отзыв пользователя на фильм из БД."""
    await review_service.delete_review_from_db(db=db, review_data=review_data)
    return {"detail": "Отзыв удален."}

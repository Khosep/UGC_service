from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.postgres import get_session
from schemas.mixins import UserIdFilmIdMixinSchema
from schemas.review_schema import (
    ReviewInDBCreate,
    ReviewInDBFull,
    ReviewInDBUpdate,
    ReviewListFind,
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


@router.post(
    "/review/show_list",
    response_model=list[ReviewInDBFull],
    status_code=HTTPStatus.OK,
    description="Получить отзывы по фильму/ отзывы по пользователю.",
)
async def get_review_list(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    review_data: ReviewListFind,
    page_number: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(
        settings.standart_page_size, description="Элементов на странице", ge=1
    ),
) -> list[ReviewInDBFull]:
    """
    Получить отзывы по фильму/ отзывы пользователя из БД с учетом оценок.

    :param page_number: Номер страницы (начиная с 1).
    :param page_size: Количество элементов на странице.
    """
    review_list = await review_service.get_list(
        db=db,
        review_data=review_data,
        page_number=page_number,
        page_size=page_size,
    )
    return review_list


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

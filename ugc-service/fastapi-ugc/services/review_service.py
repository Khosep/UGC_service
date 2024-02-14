from functools import lru_cache
from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.exceptions import (
    ReviewAlreadyExistException,
    ReviewANotFoundException,
)
from models.common import FilmReview
from schemas.mixins import UserIdFilmIdMixinSchema
from schemas.review_schema import ReviewInDBCreate, RevieInDBFull
from services.db_service import DBService, SQLAlchemyDBService


class ReviewDBService(SQLAlchemyDBService):
    model = FilmReview


class ReviewService:
    def __init__(self, db_service: Type[DBService]):
        self.db_service = db_service()

    async def create_review_in_db(
        self, db: AsyncSession, review_data: ReviewInDBCreate
    ) -> RevieInDBFull:
        """Ревью фильму от пользователя в БД."""
        try:
            new_review = await self.db_service.create(
                db=db, obj_in=review_data
            )
            return new_review
        except IntegrityError as exc:
            raise ReviewAlreadyExistException() from exc

    async def get_review_from_db(
        self, db: AsyncSession, review_data: UserIdFilmIdMixinSchema
    ) -> RevieInDBFull:
        """Получить ревью из БД."""
        stmt = select(FilmReview).where(
            FilmReview.user_id == review_data.user_id,
            FilmReview.film_id == review_data.film_id,
        )
        result = await self.db_service.execute(db=db, stmt=stmt)
        review = result.unique().scalars().first()
        if not review:
            raise ReviewANotFoundException
        return review

    async def delete_review_from_db(
        self, db: AsyncSession, review_data: UserIdFilmIdMixinSchema
    ) -> None:
        """Получить ревью из БД."""
        review = await self.get_review_from_db(db=db, review_data=review_data)
        await self.db_service.delete(db=db, obj=review)


@lru_cache()
def get_review_service() -> ReviewService:
    return ReviewService(ReviewDBService)

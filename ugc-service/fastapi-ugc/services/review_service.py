from datetime import datetime
from functools import lru_cache
from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.exceptions import (
    ReviewAlreadyExistException,
    ReviewANotFoundException,
    ReviewIdentificatorNotExistException,
    ReviewANoScoreException,
)
from models.common import FilmReview
from schemas.mixins import IdMixinSchema, UserIdFilmIdMixinSchema
from schemas.review_schema import (
    ReviewInDBCreate,
    ReviewInDBFull,
    ReviewInDBUpdate,
    ReviewListFind,
)
from services.db_service import DBService, SQLAlchemyDBService


class ReviewDBService(SQLAlchemyDBService):
    model = FilmReview


class ReviewService:
    def __init__(self, db_service: Type[DBService]):
        self.db_service = db_service()

    async def create(
        self, db: AsyncSession, review_data: ReviewInDBCreate
    ) -> ReviewInDBFull:
        """Ревью фильму от пользователя в БД."""
        try:
            if review_data.score is None:
                raise ReviewANoScoreException
            new_review = await self.db_service.create(
                db=db, obj_in=review_data
            )
            return new_review
        except IntegrityError as exc:
            raise ReviewAlreadyExistException() from exc

    async def get(
        self, db: AsyncSession, review_data: UserIdFilmIdMixinSchema
    ) -> ReviewInDBFull:
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

    async def get_list(
        self,
        db: AsyncSession,
        review_data: ReviewListFind,
        page_number: int,
        page_size: int,
    ) -> list[ReviewInDBFull]:
        """Получить список ревью из БД."""
        if review_data.user_id is None and review_data.film_id is None:
            raise ReviewIdentificatorNotExistException
        offset = (page_number - 1) * page_size
        stmt = select(FilmReview).where(
            (review_data.score_from - 1 < FilmReview.score)
            & (FilmReview.score < review_data.score_before + 1)
        )
        # Проверяем наличие user_id и film_id и добавляем условия
        if review_data.user_id:
            stmt = stmt.where(FilmReview.user_id == review_data.user_id)
        if review_data.film_id:
            stmt = stmt.where(FilmReview.film_id == review_data.film_id)
        # Добавляем пагинатор
        stmt = stmt.offset(offset).limit(page_size)
        result = await self.db_service.execute(db=db, stmt=stmt)
        review_list = result.scalars().all()
        return review_list

    async def update(
        self, db: AsyncSession, review_data: ReviewInDBUpdate
    ) -> ReviewInDBFull:
        """Обновить ревью в БД."""

        look_for_review = UserIdFilmIdMixinSchema(
            user_id=review_data.user_id, film_id=review_data.film_id
        )
        review = await self.get(db=db, review_data=look_for_review)
        modified_at = datetime.utcnow()
        obj_in = ReviewInDBFull(
            id=review.id,
            user_id=review_data.user_id,
            film_id=review_data.film_id,
            review=review_data.review or review.review,
            score=review_data.score or review.score,
            created_at=review.created_at,
            modified_at=modified_at,
        )
        result = await self.db_service.update(
            db=db, db_obj=review, obj_in=obj_in
        )
        return result

    async def delete(
        self, db: AsyncSession, review_data: UserIdFilmIdMixinSchema
    ) -> None:
        """Удалить ревью из БД."""
        review = await self.get(db=db, review_data=review_data)
        review_id = IdMixinSchema(id=review.id)
        await self.db_service.delete(db=db, obj=review_id)


@lru_cache()
def get_review_service() -> ReviewService:
    return ReviewService(ReviewDBService)

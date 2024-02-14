from functools import lru_cache
from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from core.exceptions import LikeAlreadyExistException
from models.common import Like
from schemas.like_schema import LikeInDBCreate, LikeInDBFull
from services.db_service import DBService, SQLAlchemyDBService


class LikeDBService(SQLAlchemyDBService):
    model = Like


class LikeService:
    def __init__(self, db_service: Type[DBService]):
        self.db_service = db_service()

    async def create_like_in_db(
        self, db: AsyncSession, user_id: str, film_id: str
    ) -> LikeInDBFull:
        """Ставим фильму лайк от пользователя в базе данных."""
        try:
            like_in_db = LikeInDBCreate(
                user_id=user_id, film_id=film_id, like=True
            )
            new_like = await self.db_service.create(db=db, obj_in=like_in_db)
            return new_like
        except IntegrityError as exc:
            raise LikeAlreadyExistException() from exc


@lru_cache()
def get_like_service() -> LikeService:
    return LikeService(LikeDBService)

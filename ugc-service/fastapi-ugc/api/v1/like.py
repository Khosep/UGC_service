from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas.like_schema import LikeInDBFull
from services.like_service import LikeService, get_like_service


router = APIRouter()


@router.post(
    "/like",
    response_model=LikeInDBFull,
    status_code=HTTPStatus.CREATED,
    description="Поставить лайк фильму.",
)
async def create_like(
    like_service: Annotated[LikeService, Depends(get_like_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
    user_id: str,
    film_id: str,
) -> LikeInDBFull:
    """Пользователь ставит лайк фильму."""
    new_like = await like_service.create_like_in_db(
        db=db, user_id=user_id, film_id=film_id
    )
    return new_like

from uuid import UUID

from pydantic import BaseModel, Field

from schemas.mixins import (
    CreatedMixinSchema,
    IdMixinSchema,
    UserIdFilmIdMixinSchema,
)


class ReviewInDBCreate(UserIdFilmIdMixinSchema):
    review: str
    score: int = Field(None, ge=1, le=10)


class ReviewInDBUpdate(UserIdFilmIdMixinSchema):
    review: str | None = None
    score: int | None = Field(None, ge=1, le=10)


class ReviewInDBFull(IdMixinSchema, CreatedMixinSchema, ReviewInDBCreate):
    pass


class ReviewListFind(BaseModel):
    user_id: UUID | None = None
    film_id: UUID | None = None
    score_from: int = Field(1, ge=1, le=10)
    score_before: int = Field(10, ge=1, le=10)

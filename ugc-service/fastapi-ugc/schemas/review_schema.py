from pydantic import Field

from schemas.mixins import (
    CreatedMixinSchema,
    IdMixinSchema,
    UserIdFilmIdMixinSchema,
)


class ReviewInDBCreate(UserIdFilmIdMixinSchema):
    review: str
    score: int = Field(1, ge=1, le=10)


class RevieInDBFull(IdMixinSchema, CreatedMixinSchema, ReviewInDBCreate):
    pass

from pydantic import Field, ConfigDict

from schemas.mixins import (
    CreatedMixinSchema,
    IdMixinSchema,
    UserIdFilmIdMixinSchema,
)


class ReviewInDBCreate(UserIdFilmIdMixinSchema):
    review: str
    score: int = Field(1, ge=1, le=10)


class ReviewInDBFull(IdMixinSchema, CreatedMixinSchema, ReviewInDBCreate):
    model_config = ConfigDict(from_attributes=True)

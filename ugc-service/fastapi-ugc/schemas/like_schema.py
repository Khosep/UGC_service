from uuid import UUID

from pydantic import BaseModel
from schemas.mixins import CreatedMixinSchema, IdMixinSchema


class LikeInDBCreate(BaseModel):
    user_id: UUID
    film_id: UUID
    like: bool


class LikeInDBFull(IdMixinSchema, CreatedMixinSchema, LikeInDBCreate):
    pass

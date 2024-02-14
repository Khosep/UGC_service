from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class IdMixinSchema(BaseModel):
    id: UUID


class CreatedMixinSchema(BaseModel):
    created_at: datetime
    modified_at: datetime


class UserIdFilmIdMixinSchema(BaseModel):
    user_id: UUID
    film_id: UUID

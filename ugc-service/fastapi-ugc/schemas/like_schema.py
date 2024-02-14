from schemas.mixins import (
    CreatedMixinSchema,
    IdMixinSchema,
    UserIdFilmIdMixinSchema,
)


class LikeInDBCreate(UserIdFilmIdMixinSchema):
    like: bool


class LikeInDBFull(IdMixinSchema, CreatedMixinSchema, LikeInDBCreate):
    pass

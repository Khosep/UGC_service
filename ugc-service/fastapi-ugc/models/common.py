from sqlalchemy import (
    Boolean,
    Column,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base
from models.mixins import IdMixin, TimestampMixin


class Like(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_film_like"

    user_id = Column(UUID(as_uuid=True), nullable=False)
    film_id = Column(UUID(as_uuid=True), nullable=False)
    like = Column(Boolean, default=True, nullable=False)

    UniqueConstraint(user_id, film_id, name="unique_like_from_user_to_film")

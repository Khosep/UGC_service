from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Integer,
    Text,
    UniqueConstraint,
    orm,
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


class FilmReview(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_film_review"
    user_id = Column(UUID(as_uuid=True), nullable=False)
    film_id = Column(UUID(as_uuid=True), nullable=False)
    review = Column(Text, nullable=False)
    score = Column(
        Integer,
        CheckConstraint("score > 0 AND score < 11"),
        default=1,
        nullable=False,
    )

    @orm.validates("score")
    def validate_score(self, key, value):
        if not 0 < value < 11:
            raise ValueError(f"Invalid score {value}")
        return value

    UniqueConstraint(user_id, film_id, name="unique_reviev_from_user_to_film")

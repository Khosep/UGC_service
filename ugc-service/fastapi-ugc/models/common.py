from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Integer,
    Text,
    UniqueConstraint,
    orm,
)

from db.postgres import Base
from models.mixins import IdMixin, TimestampMixin, UserIdFilmIdMixin


class Like(Base, IdMixin, TimestampMixin, UserIdFilmIdMixin):
    __tablename__ = "user_film_like"

    like = Column(Boolean, default=True, nullable=False)

    UniqueConstraint(user_id, film_id, name="unique_like_from_user_to_film")  # noqa


class FilmReview(Base, IdMixin, TimestampMixin, UserIdFilmIdMixin):
    __tablename__ = "user_film_review"

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

    UniqueConstraint(user_id, film_id, name="unique_reviev_from_user_to_film")  # noqa

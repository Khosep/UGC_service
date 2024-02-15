"""Проверка удадения ролей у пользователя."""
from http import HTTPStatus
from typing import Callable

from functional.test_data.review_data import (
    error_reviews,
    reviews,
    check_reviews_in_db_sql,
)


async def test_create_review(
    create_review: Callable, get_review_from_bd: Callable, db_fetch: Callable
) -> None:
    """Создаем отзыв."""
    response = await create_review(review_data=reviews[0])
    assert response["status"] == HTTPStatus.CREATED
    review_in_db = await db_fetch(check_reviews_in_db_sql)
    assert len(review_in_db) == 1
    review_from_bd = await get_review_from_bd(
        field="user_id", value=reviews[0]["user_id"]
    )
    assert str(review_from_bd["user_id"]) == reviews[0]["user_id"]
    assert str(review_from_bd["film_id"]) == reviews[0]["film_id"]
    assert review_from_bd["review"] == reviews[0]["review"]
    assert review_from_bd["score"] == reviews[0]["score"]


async def test_create_review_without_data(
    create_review: Callable, db_fetch: Callable
) -> None:
    """Создаем отзыв без необходимых данных."""
    response = await create_review(review_data=error_reviews[0])
    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["body"] == {
        "detail": "Ошибки по полям: ['user_id: Field required', 'film_id: "
        "Field required', 'review: Field required']."
    }

    response = await create_review(review_data=error_reviews[1])
    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["body"] == {
        "detail": "Ошибки по полям: ['user_id: Field required']."
    }

    response = await create_review(review_data=error_reviews[2])
    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["body"] == {
        "detail": "Ошибки по полям: ['film_id: Field required']."
    }

    response = await create_review(review_data=error_reviews[3])
    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["body"] == {
        "detail": "Ошибки по полям: ['review: Field required']."
    }

    response = await create_review(review_data=error_reviews[4])
    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response["body"] == {
        "detail": "Ошибки по полям: ['score: Field required']."
    }
    review_in_db = await db_fetch(check_reviews_in_db_sql)
    assert len(review_in_db) == 0


async def test_create_review_override(
    create_review: Callable, db_fetch: Callable
) -> None:
    """Создаем повторно отзыв."""
    await create_review(review_data=reviews[0])
    response = await create_review(review_data=reviews[0])
    assert response["status"] == HTTPStatus.BAD_REQUEST
    assert response["body"] == {
        "detail": "Вы уже оставили отзыв к этому фильму ранее."
    }
    review_in_db = await db_fetch(check_reviews_in_db_sql)
    assert len(review_in_db) == 1

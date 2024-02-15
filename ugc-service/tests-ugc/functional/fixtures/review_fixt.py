from typing import Callable
import orjson
import pytest
from asyncpg import Connection

from functional.settings import test_settings

ENDPOINT_SHOW = (
    f"{test_settings.endpoint_common_reviews}{test_settings.endpoint_show}"
)
ENDPOINT_SHOW_LIST = f"{test_settings.endpoint_common_reviews}{test_settings.endpoint_show_list}"


@pytest.fixture
def create_review(make_post_request: Callable) -> Callable:
    """Создаем отзыв."""

    async def inner(review_data: dict | None = None) -> dict:
        response = await make_post_request(
            headers=test_settings.headers_common,
            data=orjson.dumps(review_data),
            endpoint=test_settings.endpoint_common_reviews,
        )
        return response

    return inner


@pytest.fixture
def show_review(make_post_request: Callable) -> Callable:
    """Показать отзыв."""

    async def inner(review_data: dict | None = None) -> dict:
        response = await make_post_request(
            headers=test_settings.headers_common,
            data=orjson.dumps(review_data),
            endpoint=ENDPOINT_SHOW,
        )
        return response

    return inner


@pytest.fixture
def show_review_list(make_post_request: Callable) -> Callable:
    """Показать список отзывов."""

    async def inner(review_data: dict | None = None) -> dict:
        response = await make_post_request(
            headers=test_settings.headers_common,
            data=orjson.dumps(review_data),
            endpoint=ENDPOINT_SHOW_LIST,
        )
        return response

    return inner


@pytest.fixture
def get_review_from_bd(db_conn: Connection):
    """Получить отзыв из БД."""

    async def inner(field: str, value: str) -> dict:
        sql = f"SELECT * FROM user_film_review WHERE {field} = '{value}';"
        result = await db_conn.fetchrow(sql)
        return result

    return inner


@pytest.fixture
def update_review(make_patch_request: Callable) -> Callable:
    """Измеенние отзыва."""

    async def inner(review_data: dict | None = None) -> dict:
        response = await make_patch_request(
            headers=test_settings.headers_common,
            data=orjson.dumps(review_data),
            endpoint=test_settings.endpoint_common_reviews,
        )
        return response

    return inner


@pytest.fixture
def delete_review(make_delete_request: Callable) -> Callable:
    """Удаление отзыва."""

    async def inner(review_data: dict | None = None) -> dict:
        response = await make_delete_request(
            headers=test_settings.headers_common,
            data=orjson.dumps(review_data),
            endpoint=test_settings.endpoint_common_reviews,
        )
        return response

    return inner

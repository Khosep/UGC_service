from http import HTTPStatus
from typing import Callable

from functional.settings import test_settings
from functional.test_data.film_data import film_data
from functional.test_data.token_data import token_data


async def test_create_record_with_token(
    create_film_stats_record: Callable, create_token: Callable
):
    """Проверка создания новой записи с токеном."""
    token = create_token(token_data)
    authorization = {"Authorization": f"Bearer {token}"}
    headers = test_settings.headers_common.copy()
    headers.update(authorization)
    response = await create_film_stats_record(
        film_data=film_data,
        headers=headers,
    )
    assert response["status"] == HTTPStatus.CREATED


async def test_create_record_without_token(create_film_stats_record: Callable):
    """Проверка создания новой записи без токена."""
    response = await create_film_stats_record(film_data=film_data)
    assert response["status"] == HTTPStatus.CREATED

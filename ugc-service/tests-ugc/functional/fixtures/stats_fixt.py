from typing import Callable
import orjson
import pytest

from functional.settings import test_settings


@pytest.fixture
def create_film_stats_record(make_post_request: Callable) -> None:
    """Следать запись статуса просмотра фильма пользователем."""

    async def inner(
        headers: dict | None = test_settings.headers_common,
        film_data: dict | None = None,
    ) -> dict:
        response = await make_post_request(
            headers=headers,
            data=orjson.dumps(film_data),
            endpoint=test_settings.common_endpoint,
        )
        return response

    return inner

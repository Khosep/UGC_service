import pytest
from jose import jwt

from functional.settings import test_settings


@pytest.fixture
def create_token() -> None:
    """Создаем токен."""

    def inner(data: dict) -> str:
        encoded_jwt = jwt.encode(
            data,
            test_settings.access_token_secret_key,
            algorithm=test_settings.token_jwt_algorithm,
        )
        return encoded_jwt

    return inner

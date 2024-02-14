import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )
    # Настройки подключения к БД
    django_postgres_db: str = Field(default="movies_database")
    django_postgres_user: str = Field(default="app")
    django_postgres_password: str = Field(default="123qwe")
    django_postgres_host: str = Field(default="127.0.0.1")
    django_postgres_port: int = Field(default=5432)
    # Настройки Django
    django_secret_key: str = Field(default="default_key")
    django_debug: bool = Field(default=True)
    django_allowed_hosts: list[str] = Field(default=["127.0.0.1"])
    django_swagger_port: int = Field(default=8080)

    # Настройки auth-сервиса
    django_auth_api_host: str = Field(default="127.0.0.1")
    django_auth_api_path: str = Field(default="auth/v1/auth/login/")

    django_access_token_secret_key: str = Field(
        default="ACCESS_TOKEN_SECRET_KEY"
    )
    django_token_jwn_algoritm: str = Field(default="HS256")


settings_django = Settings()

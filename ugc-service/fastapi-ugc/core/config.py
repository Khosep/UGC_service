import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )
    # Настройки Fastapi
    ugc_fastapi_host: str = Field(default="127.0.0.1")
    ugc_fastapi_port: int = Field(default=7005)
    # Настройки Swagger-документации
    project_name: str = Field(default="ugc-service")
    version: str = "0.1.0"
    description: str = "Пользователи сервиса"
    openapi_docs_url: str = "/ugc/openapi"
    openapi_url: str = "/ugc/openapi.json"
    prefix: str = "/ugc/v1"

    # Настройки токенов
    access_token_secret_key: str = Field(default="ACCESS_TOKEN_SECRET_KEY")
    token_jwt_algorithm: str = "HS256"

    request_limit_per_minute: int = 20

    session_cookie: str = "your_session_cookie"

    enable_tracer: bool = Field(default=False)

    # Настройка kafka
    kafka_host: str = Field(default="127.0.0.1")
    kafka_port: int = Field(default=9094)
    kafka_topic_timestamp: str = "user_film_timestamp"

    @property
    def dsn(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme=self.scheme,
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )


settings = Settings()

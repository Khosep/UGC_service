import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(os.path.dirname(BASE_DIR), ".env")
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )

    batch_size: int = 5

    # Настройка kafka
    kafka_host: str = Field(default="127.0.0.1")
    kafka_port: int = Field(default=9094)
    kafka_topic_timestamp: str = "user_film_timestamp"

    # Настройка ClickHouse
    clickhouse_host: str = Field(default='127.0.0.1')


settings = Settings()

from pydantic import Field, HttpUrl, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict()

    project_name: str = Field(default="test_ugc")

    ugc_test_redis_host: str = Field(default="127.0.0.1")
    ugc_test_redis_port: int = Field(default=5380)

    ugc_test_fastapi_host: str = Field(default="127.0.0.1")
    ugc_test_fastapi_port: int = Field(default=7001)

    ugc_test_postgres_host: str = Field(default="127.0.0.1")
    ugc_test_postgres_port: int = Field(default=4433)
    ugc_test_postgres_db: str = Field(default="ugc_database")
    ugc_test_postgres_user: str = Field(default="app")
    ugc_test_postgres_password: str = Field(default="123qwe")

    @property
    def app_url(self) -> HttpUrl:
        return (
            f"http://{self.ugc_test_fastapi_host}:"
            f"{self.ugc_test_fastapi_port}"
        )

    @property
    def redis_dsn(self) -> RedisDsn:
        return f"redis://{self.ugc_test_redis_host}:{self.ugc_test_redis_port}"

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return (
            f"postgresql://{self.ugc_test_postgres_user}:{self.ugc_test_postgres_password}@"
            f"{self.ugc_test_postgres_host}:{self.ugc_test_postgres_port}/"
            f"{self.ugc_test_postgres_db}"
        )

    #  endpoint paths
    endpoint_common_reviews: str = "/ugc/v1/review"
    endpoint_show: str = "/show"
    endpoint_show_list: str = "/show_list"

    headers_common: dict = {
        "Content-Type": "application/json",
    }


test_settings = TestSettings()

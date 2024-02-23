from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict()

    project_name: str = Field(default="test_ugc")

    ugc_fastapi_host: str = Field(default="127.0.0.1")
    ugc_fastapi_port: int = Field(default=7007)

    @property
    def app_url(self) -> HttpUrl:
        return f"http://{self.ugc_fastapi_host}:" f"{self.ugc_fastapi_port}"

    #  endpoint paths
    common_endpoint: str = "/ugc/v1/stats"

    headers_common: dict = {
        "Content-Type": "application/json",
        "X-Request-Id": "1",
    }

    access_token_secret_key: str = Field(default="ACCESS_TOKEN_SECRET_KEY")
    token_jwt_algorithm: str = Field(default="HS256")


test_settings = TestSettings()

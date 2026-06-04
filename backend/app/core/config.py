from functools import lru_cache
from os import getenv

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "tartip-backend"
    app_version: str = "0.1.0"
    app_env: str = getenv("APP_ENV", "local")
    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+psycopg://tartip:tartip_local_password@postgres:5432/tartip",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

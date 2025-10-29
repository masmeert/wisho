from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
        env_file=ENV_FILE,
    )

    echo: bool = False
    future: bool = True
    expire_on_commit: bool = False

    hostname: str = "localhost"
    port: int = 5432
    user: str = "wisho"
    password: str = "wisho"  # noqa: S105
    name: str = "wisho_db"

    @property
    def uri(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+psycopg2",
            host=self.hostname,
            username=self.user,
            password=self.password,
            port=self.port,
            path=self.name or "",
        )
        return str(dsn)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=ENV_FILE,
    )

    port: int = 8000
    cors_allow_origins: str = "http://localhost:3000"

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    @property
    def cors_origins(self) -> list[str]:
        return [url.strip() for url in self.cors_allow_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings

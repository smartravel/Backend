from urllib.parse import quote_plus

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class CORS(BaseModel):
    origins: list[str] = ["http://localhost:5173"]


class Database(BaseModel):
    postgres_username: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    alembic_postgres_host: str | None = None
    echo: bool = False

    def _url(self, host: str) -> str:
        password = quote_plus(self.postgres_password)
        return (
            f"postgresql+asyncpg://{self.postgres_username}:{password}"
            f"@{host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_database_url(self) -> str:
        return self._url(self.postgres_host)

    @property
    def alembic_url(self) -> str:
        return self._url(self.alembic_postgres_host or self.postgres_host)


class JWT(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class Cookies(BaseModel):
    secure: bool = False


class Redis(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    db: int = 0


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="config.toml",
        env_nested_delimiter="__",
        extra="ignore",
    )

    database: Database
    jwt: JWT
    cors: CORS = CORS()
    cookies: Cookies = Cookies()
    redis: Redis = Redis()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, env_settings, TomlConfigSettingsSource(settings_cls))


config = Config()
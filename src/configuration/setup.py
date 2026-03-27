from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Authentication(BaseSettings):
    AUTHENTICATION: bool = False
    AUTHENTICATION_HTTP_BASIC_USERNAME: str | None = None
    AUTHENTICATION_HTTP_BASIC_PASSWORD: str | None = None


class Cryptography(BaseSettings):
    CRYPTOGRAPHY: bool = False
    CRYPTOGRAPHY_SECRET_KEY: str | None = None


class Postgres(BaseSettings):
    POSTGRES: bool = False
    POSTGRES_HOST: str | None = None

    @property
    def psycopg(self) -> str | None:
        return self.POSTGRES_HOST.replace("asyncpg", "psycopg2") if self.POSTGRES_HOST else None

    @property
    def asyncpg(self) -> str | None:
        return self.POSTGRES_HOST


class Redis(BaseSettings):
    REDIS: bool = False
    REDIS_HOST: str | None = None


class Jwt(BaseSettings):
    JWT: bool = False
    JWT_ALGORITHM: str | None = "HS256"
    JWT_SECRET_KEY: str | None = None
    JWT_ACCESS_EXPIRED_SECONDS: int | None = 43200  # 12h
    JWT_REFRESH_EXPIRED_SECONDS: int | None = 2592000  # 30d


class Logging(BaseSettings):
    LOGGING: bool = True


configs = [
    Authentication,
    Cryptography,
    Logging,
    Postgres,
    Redis,
    Jwt,
]


class Settings(*configs):  # type:ignore
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()

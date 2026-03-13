from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Authentication(BaseSettings):
    AUTHENTICATION: bool = False
    AUTHENTICATION_HTTP_BASIC_USERNAME: str | None = None
    AUTHENTICATION_HTTP_BASIC_PASSWORD: str | None = None


class Cryptography(BaseSettings):
    CRYPTOGRAPHY: bool = False
    CRYPTOGRAPHY_SECRET_KEY: str | None = None


class Scheduler(BaseSettings):
    SCHEDULER: bool = False


class Postgres(BaseSettings):
    POSTGRES: bool = False
    POSTGRES_HOST: str | None = None

    @property
    def psycopg(self) -> str | None:
        return self.POSTGRES_HOST.replace("asyncpg", "psycopg2") if self.POSTGRES_HOST else None

    @property
    def asyncpg(self) -> str | None:
        return self.POSTGRES_HOST


class Telegram(BaseSettings):
    TELEGRAM: bool = False
    TELEGRAM_ACCOUNT_ID: int | None = Field(None, description="Account ID in Telegram")
    TELEGRAM_ACCOUNT_API_ID: int | None = Field(None, description="Telethon Client in my.telegram")
    TELEGRAM_ACCOUNT_API_HASH: str | None = Field(None, description="Telethon Client in my.telegram")
    TELEGRAM_BOT_ID: int | None = Field(None, description="Bot ID in Telegram in BotFather")
    TELEGRAM_BOT_TOKEN: str | None = Field(None, description="Bot sign-in in BotFather")


class Logging(BaseSettings):
    LOGGING: bool = True


class Sentry(BaseSettings):
    SENTRY: bool = False
    SENTRY_ENV: str = "default"
    SENTRY_DSN: str | None = None


class Redis(BaseSettings):
    REDIS: bool = False
    REDIS_HOST: str | None = None


class Jwt(BaseSettings):
    JWT: bool = False
    JWT_ALGORITHM: str | None = "HS256"
    JWT_SECRET_KEY: str | None = None
    JWT_ACCESS_EXPIRED_SECONDS: int | None = 43200  # 12h
    JWT_REFRESH_EXPIRED_SECONDS: int | None = 2592000  # 30d


configs = [
    Authentication,
    Cryptography,
    Scheduler,
    Postgres,
    Telegram,
    Logging,
    Sentry,
    Redis,
    Jwt,
]


class Settings(*configs):  # type:ignore
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    DOMAIN: str = "http://localhost"


settings = Settings()

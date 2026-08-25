from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_csrf_protect import CsrfProtect

load_dotenv(override=True)


class CSRFSettings(BaseSettings):
    secret_key: str = Field(..., alias="CSRF_SECRET_KEY")
    cookie_samesite: str = Field(..., alias="CSRF_COOKIE_SAMESITE")


@CsrfProtect.load_config
def get_csrf_config():
    return CSRFSettings()


class AccessTokenSettings(BaseSettings):
    TOKEN_LIFETIME_SECONDS: int = Field(..., alias="TOKEN_LIFETIME_SECONDS")
    RESET_PASSWORD_TOKEN_SECRET: str = Field(..., alias="RESET_PASSWORD_TOKEN_SECRET")
    VERIFICATION_TOKEN_SECRET: str = Field(..., alias="VERIFICATION_TOKEN_SECRET")


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    access_token: AccessTokenSettings = AccessTokenSettings()


settings = Settings()

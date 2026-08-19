from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


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

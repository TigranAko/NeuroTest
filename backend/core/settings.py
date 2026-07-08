from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    TAVILY_API_KEY: SecretStr
    CEREBRAS_API_KEY: SecretStr
    OPENROUTER_API_KEY: SecretStr


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    auth_jwt_secret: str
    auth_algorithm: str = "HS256"
    auth_access_expire_minutes: int = 15
    auth_refresh_expire_days: int = 7


auth_settings = AuthSettings()
settings = LLMSettings()

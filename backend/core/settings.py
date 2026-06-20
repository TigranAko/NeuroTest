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


settings = LLMSettings()

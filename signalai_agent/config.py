from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SIGNALAI_", env_file=".env", extra="ignore")

    service_name: str = "signalai-agent"
    service_version: str = "0.1.0"
    capability_base_url: AnyHttpUrl = "http://signalai-server:3000"
    capability_timeout_seconds: float = Field(default=30.0, gt=0, le=300)
    llm_base_url: AnyHttpUrl | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    llm_timeout_seconds: float = Field(default=60.0, gt=0, le=300)
    max_steps: int = Field(default=8, ge=1, le=32)
    service_token: str | None = None


settings = Settings()

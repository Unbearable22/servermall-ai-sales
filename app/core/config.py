from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./servermall.db"
    admin_api_key: str = "replace-with-a-long-random-secret"
    allow_outreach: bool = False
    llm_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_manager_chat_id: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

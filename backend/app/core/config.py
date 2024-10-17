import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # General Settings
    PROJECT_NAME: str = "News AIgency"
    API_VERSION: str = "v1"
    LITE_LLM_KEY: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), ".env"), extra="allow")

    # Qdrant DB settings

settings = Settings()
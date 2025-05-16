import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General Settings
    PROJECT_NAME: str = "News AIgency"
    API_VERSION: str = "v1"
    LITE_LLM_KEY: str
    # Can be "development" or "release"
    ENVIRONMENT: str

    SCRAPER: str = "jina"  # can be "playwright" or "jina"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"), extra="allow"
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "15432"


settings = Settings()
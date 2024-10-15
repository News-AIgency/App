from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General Settings
    PROJECT_NAME: str = "News AIgency"
    API_VERSION: str = "v1"

    # Qdrant DB settings

    # TODO: LiteLLM Api key?



settings = Settings()

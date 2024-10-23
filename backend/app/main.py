from functools import lru_cache
from typing import Annotated

import uvicorn
from App.backend.app.api.v1.endpoints import topic_to_article, url_to_topic
from core.config import Settings, settings
from fastapi import Depends, FastAPI
from services.ai_service.litellm_service import LiteLLMService

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# Routing
app.include_router(url_to_topic.router)
app.include_router(topic_to_article.router)


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Health check endpoint
@app.get("/health")
def health_check() -> dict:
    return {"status": "OK"}


@app.get("/info")
async def info(info_settings: Annotated[Settings, Depends(get_settings)]) -> dict:
    return {
        "app_name": info_settings.PROJECT_NAME,
        "version": info_settings.API_VERSION,
    }


@app.get("/use-litellm")
def use_litellm_key() -> dict:
    ai_service = LiteLLMService()
    return {"LiteLLM Response": ai_service.test_litellm()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

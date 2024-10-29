# Add the 'App' directory (parent of 'backend') to sys.path
import os
import sys

from backend.app.services.ai_service.response_models import TestLiteLLMPoem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from functools import lru_cache
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI

from backend.app.api.main import api_router
from backend.app.core.config import Settings, settings
from backend.app.services.ai_service.litellm_service import LiteLLMService

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# Routing
app.include_router(api_router)


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
async def use_litellm_key() -> TestLiteLLMPoem:
    ai_service = LiteLLMService()
    return await ai_service.test_litellm()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

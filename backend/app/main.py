import os
import sys
from contextlib import asynccontextmanager

# Add the 'App' directory (parent of 'backend') to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from backend.app.api.main import api_router
from backend.app.core.config import Settings, settings
from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import TestLiteLLMPoem


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.API_VERSION, lifespan=lifespan
)

# Routing
app.include_router(api_router)

# CORS - testing only
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

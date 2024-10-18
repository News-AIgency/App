from functools import lru_cache
from typing import Annotated

from core.config import Settings, settings
from fastapi import Depends, FastAPI
from services.ai_service.litellm_service import use_litellm

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# Routing
# app.include_router(scrape.router, prefix="/api/v1/scrape", tags=["scrape"])
# app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
# app.include_router(frontend.router, prefix="/api/v1/frontend", tags=["frontend"])
# app.include_router(qdrant.router, prefix="/api/v1/qdrant", tags=["qdrant"])


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
    return {"LiteLLM Response": use_litellm()}

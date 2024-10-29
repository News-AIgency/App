from fastapi import APIRouter, HTTPException
from fastapi_cache import FastAPICache

from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import ArticleResponse
from backend.app.utils.default_article import default_article

router = APIRouter()


# Temporary get and post method at the same time
@router.post("/article/generate", response_model=ArticleResponse)
@router.get("/article/generate", response_model=ArticleResponse)
async def extract_article(
    url: str = default_article,
) -> ArticleResponse:
    try:
        cache_key = f"fastapi-cache:extract_topics:{url}"
        cached_content = await FastAPICache.get_backend().get(cache_key)

        # Temporary solution until scraper works again, change logic once it works
        scraped_article = "Article is missing"
        if cached_content:
            scraped_article = cached_content
        elif url == default_article:
            scraped_article = default_article

        ai_service = LiteLLMService()
        article = await ai_service.generate_article(scraped_article)

        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

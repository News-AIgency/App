from fastapi import APIRouter, HTTPException
from fastapi_cache import FastAPICache

from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import TopicsResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.default_article import default_article, default_article_url

router = APIRouter()


# Temporary default url for testing purposes, temporary get and post method at the same time
@router.post("/article/topics", response_model=TopicsResponse)
@router.get("/article/topics", response_model=TopicsResponse)
async def extract_topics(
    url: str = default_article,
) -> TopicsResponse:
    try:
        cache_key = f"article:{url}"
        default_cache_key = f"article:{default_article_url}"
        cached_content = await FastAPICache.get_backend().get(cache_key)

        # Temporary solution until scraper works again
        if not cached_content:
            if url == default_article:
                scraped_content = url
                await FastAPICache.get_backend().set(
                    default_cache_key, scraped_content, expire=3600
                )
            else:
                scraped_content = await jina_scrape(url)
                await FastAPICache.get_backend().set(
                    cache_key, scraped_content, expire=3600
                )
        else:
            scraped_content = cached_content

        ai_service = LiteLLMService()
        generated_topics = await ai_service.generate_topics(scraped_content)

        return generated_topics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

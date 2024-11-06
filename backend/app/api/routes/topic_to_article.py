from fastapi import APIRouter, HTTPException, Request
from fastapi_cache import FastAPICache

from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import ArticleResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.default_article import default_article, default_topic

router = APIRouter()


# @router.get("/article/generate", response_model=ArticleResponse)
@router.post("/article/generate", response_model=ArticleResponse)
async def extract_article(request: Request) -> ArticleResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)

        cache_key = f"article:{url}"
        default_cache_key = f"article:{default_article}"
        cached_content = await FastAPICache.get_backend().get(cache_key)

        if not cached_content:
            if url == default_article:
                scraped_article = url
                await FastAPICache.get_backend().set(
                    default_cache_key, scraped_article, expire=3600
                )
            else:
                scraped_article = await jina_scrape(url)
                await FastAPICache.get_backend().set(
                    cache_key, scraped_article, expire=3600
                )
        else:
            scraped_article = cached_content

        ai_service = LiteLLMService()
        article = await ai_service.generate_article(scraped_article, selected_topic)

        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

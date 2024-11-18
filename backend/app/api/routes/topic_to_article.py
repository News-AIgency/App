from fastapi import APIRouter, HTTPException, Request
from fastapi_cache import FastAPICache

from backend.app.core.config import settings
from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import ArticleResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.default_article import (
    default_article,
    default_engaging_text,
    default_headline,
    default_headlines,
    default_topic,
)

router = APIRouter()


# region Extract article
async def extract_article(
    url: str = default_article, selected_topic: str = default_topic
) -> ArticleResponse:
    try:
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


if settings.ENVIRONMENT == "development":

    @router.get("/article/generate", response_model=ArticleResponse)
    async def extract_article_get(
        url: str = default_article, selected_topic: str = default_topic
    ) -> ArticleResponse:
        return await extract_article(url, selected_topic)


@router.post("/article/generate", response_model=ArticleResponse)
async def extract_article_post(
    request: Request,
) -> ArticleResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        return await extract_article(url, selected_topic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region Headlines
async def regenerate_headlines(
    url: str = default_article,
    selected_topic: str = default_topic,
    old_headlines: str = None,
) -> ArticleResponse:
    try:
        old_headlines_list = (
            old_headlines.split("|") if old_headlines else default_headlines
        )

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
        new_headlines = await ai_service.regenerate_headlines(
            scraped_article, selected_topic, old_headlines_list
        )

        return new_headlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/headlines", response_model=ArticleResponse)
    async def regenerate_headlines_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_headlines: str = None,
    ) -> ArticleResponse:
        return await regenerate_headlines(url, selected_topic, old_headlines)


@router.post("/regenerate/headlines", response_model=ArticleResponse)
async def regenerate_headlines_post(
    request: Request,
) -> ArticleResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_headlines = request_body.get("old_headlines")

        return await regenerate_headlines(url, selected_topic, old_headlines)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region Engaging text
async def regenerate_engaging_text(
    url: str = default_article,
    selected_topic: str = default_topic,
    old_engaging_text: str = default_engaging_text,
    current_headline: str = default_headline,
) -> ArticleResponse:
    try:
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
        new_engaging_text = await ai_service.regenerate_engaging_text(
            scraped_article, selected_topic, old_engaging_text, current_headline
        )

        return new_engaging_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "production":

    @router.get("/regenerate/engaging_text", response_model=ArticleResponse)
    async def regenerate_engaging_text_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_engaging_text: str = default_engaging_text,
        current_headline: str = default_headline,
    ) -> ArticleResponse:
        return await regenerate_engaging_text(
            url, selected_topic, old_engaging_text, current_headline
        )


@router.post("/regenerate/engaging_text", response_model=ArticleResponse)
async def regenerate_engaging_text_post(
    request: Request,
) -> ArticleResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_engaging_text = request_body.get("old_engaging_text", default_engaging_text)
        current_headline = request_body.get("current_headline", default_headline)

        return await regenerate_engaging_text(
            url, selected_topic, old_engaging_text, current_headline
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion

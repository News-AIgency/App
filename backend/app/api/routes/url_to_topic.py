from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request
from fastapi_cache import FastAPICache
from starlette.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.services.ai_service.article_generator import ArticleGenerator
from backend.app.services.ai_service.response_models import TopicsResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.default_article import default_article, default_article_url

router = APIRouter()


# region Url domain validation
async def url_validate(
    url: str = default_article_url,
    hostnames: list[str] = None,
) -> JSONResponse:
    # List of trustworthy sources
    if hostnames is None:
        hostnames = ["slovak.statistics.sk"]

    try:
        result = urlparse(url)
        if result.hostname not in hostnames:
            raise HTTPException(
                status_code=400,
                detail=f"The hostname {result.hostname} is not allowed.",
            )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL")
    return JSONResponse(content={"detail": url})


if settings.ENVIRONMENT == "development":

    @router.get("/url-validate")
    async def url_validate_get(
        url: str = default_article_url,
        hostnames: list[str] = None,
    ) -> JSONResponse:
        return await url_validate(url)


@router.post("/url-validate")
async def url_validate_post(
    request: Request,
) -> JSONResponse:
    request_body = await request.json()
    url = request_body.get("url", default_article_url)
    return await url_validate(url)


# endregion


# region Extract topics
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

        ai_service = ArticleGenerator()
        generated_topics = await ai_service.generate_topics(scraped_content)

        return generated_topics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/article/topics", response_model=TopicsResponse)
async def extract_topics_post(
    request: Request,
) -> TopicsResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        return await extract_topics(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/article/topics", response_model=TopicsResponse)
    async def extract_topics_get(
        url: str = default_article,
    ) -> TopicsResponse:
        return await extract_topics(url)


# endregion

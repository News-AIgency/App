import asyncio
import os
import traceback

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from backend.app.core.config import settings
from backend.app.services.ai_service.article_generator import ArticleGenerator
from backend.app.services.ai_service.response_models import (
    ArticleBodyResponse,
    EngagingTextResponse,
    ExtractArticleResponse,
    HeadlineResponse,
    PerexResponse,
    TagsResponse,
)
from backend.app.utils.default_article import (
    default_article,
    default_article_url,
    default_engaging_text,
    default_headline,
    default_headlines,
    default_perex,
    default_tags,
    default_topic,
)
from backend.app.utils.scraping_cache_functions import cache_or_scrape
from backend.app.utils.url_getter import extract_reference_urls

router = APIRouter()


# region Extract article
async def extract_article(
    url: str = default_article_url,
    selected_topic: str = default_topic,
    storm: bool = False,
) -> ExtractArticleResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article_url)

        storm_article = None
        if storm:
            storm_article = await storm_cache_retrieve(selected_topic, url)

        ai_service = ArticleGenerator()
        article = await ai_service.generate_article(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            storm_article=storm_article,
        )
        
        storm_urls = None
        if storm_article:
            storm_urls = extract_reference_urls(storm_article)

        article_data = None
        if article.gen_graph:
            graph_labels_key = "x_vals" if article.graph_type == "scatter" else "labels"
            graph_values_key = "y_vals" if article.graph_type == "scatter" else "values"

            article_data = {
                "url": {"url": url},
                "heading": {"heading_content": article.headlines[0]},
                "topic": {"topic_content": selected_topic},
                "perex": {"perex_content": article.perex},
                "body": {"body_content": article.article},
                "engaging_text": {"engaging_text_content": article.engaging_text},
                "tags": [{"tags_content": tag} for tag in article.tags],
                "graph_data": {
                    "graph_type": article.graph_type,
                    "graph_labels": article.graph_data[graph_labels_key],
                    "graph_values": article.graph_data[graph_values_key],
                },
            }

        verify_ssl = settings.ENVIRONMENT != "development"
        async with httpx.AsyncClient(verify=verify_ssl) as client:
            response = await client.post(
                "https://api.wraite.news/save_article/", json=article_data
            )

        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        response_data = response.json()
        return ExtractArticleResponse(id=response_data.get("id"), article=article, storm_urls = storm_urls)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/article/generate", response_model=ExtractArticleResponse)
    async def extract_article_get(
        url: str = default_article_url,
        selected_topic: str = default_topic,
        storm: bool = False,
    ) -> ExtractArticleResponse:
        return await extract_article(url, selected_topic, storm)


@router.post("/article/generate", response_model=ExtractArticleResponse)
async def extract_article_post(
    request: Request,
) -> ExtractArticleResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article_url)
        selected_topic = request_body.get("selected_topic", default_topic)
        storm = request_body.get("storm", False)
        return await extract_article(url, selected_topic, storm)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region Headlines
async def regenerate_headlines(
    url: str = default_article_url,
    selected_topic: str = default_topic,
    old_headlines: list[str] = default_headlines,
) -> HeadlineResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article_url)

        ai_service = ArticleGenerator()
        new_headlines = await ai_service.generate_headlines(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            old_headlines=old_headlines,
        )

        return new_headlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/headlines", response_model=HeadlineResponse)
    async def regenerate_headlines_get(
        url: str = default_article_url,
        selected_topic: str = default_topic,
        old_headlines: list[str] = default_headlines,
    ) -> HeadlineResponse:
        return await regenerate_headlines(url, selected_topic, old_headlines)


@router.post("/regenerate/headlines", response_model=HeadlineResponse)
async def regenerate_headlines_post(
    request: Request,
) -> HeadlineResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article_url)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_headlines = request_body.get("old_headlines")

        return await regenerate_headlines(url, selected_topic, old_headlines)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region Engaging text
async def regenerate_engaging_text(
    url: str = default_article_url,
    selected_topic: str = default_topic,
    old_engaging_text: str = default_engaging_text,
    current_headline: str = default_headline,
    storm: bool = False,
) -> EngagingTextResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article_url)

        storm_article = None
        if storm:
            storm_article = await storm_cache_retrieve(selected_topic, url)

        ai_service = ArticleGenerator()
        new_engaging_text = await ai_service.generate_engaging_text(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            old_engaging_text=old_engaging_text,
            current_headline=current_headline,
            storm_article=storm_article,
        )

        # Ulozit engaging text do DB
        return new_engaging_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/engaging_text", response_model=EngagingTextResponse)
    async def regenerate_engaging_text_get(
        url: str = default_article_url,
        selected_topic: str = default_topic,
        old_engaging_text: str = default_engaging_text,
        current_headline: str = default_headline,
        storm: bool = False,
    ) -> EngagingTextResponse:
        return await regenerate_engaging_text(
            url, selected_topic, old_engaging_text, current_headline, storm
        )


@router.post("/regenerate/engaging_text", response_model=EngagingTextResponse)
async def regenerate_engaging_text_post(
    request: Request,
) -> EngagingTextResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article_url)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_engaging_text = request_body.get("old_engaging_text", default_engaging_text)
        current_headline = request_body.get("current_headline", default_headline)
        storm = request_body.get("storm", False)

        return await regenerate_engaging_text(
            url, selected_topic, old_engaging_text, current_headline, storm
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region Perex
async def regenerate_perex(
    url: str = default_article_url,
    selected_topic: str = default_topic,
    old_perex: str = default_perex,
    current_headline: str = default_headline,
    storm: bool = False,
) -> PerexResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article_url)

        storm_article = None
        if storm:
            storm_article = await storm_cache_retrieve(selected_topic, url)

        ai_service = ArticleGenerator()
        new_perex = await ai_service.generate_perex(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            old_perex=old_perex,
            current_headline=current_headline,
            storm_article=storm_article,
        )

        # ulozit perex do DB
        return new_perex
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/perex", response_model=PerexResponse)
    async def regenerate_perex_get(
        url: str = default_article_url,
        selected_topic: str = default_topic,
        old_perex: str = default_perex,
        current_headline: str = default_headline,
        storm: bool = False,
    ) -> PerexResponse:
        return await regenerate_perex(
            url, selected_topic, old_perex, current_headline, storm
        )


@router.post("/regenerate/perex", response_model=PerexResponse)
async def regenerate_perex_post(
    request: Request,
) -> PerexResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article_url)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_perex = request_body.get("old_perex", default_perex)
        current_headline = request_body.get("current_headline", default_headline)
        storm = request_body.get("storm", False)

        return await regenerate_perex(
            url, selected_topic, old_perex, current_headline, storm
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region ArticleBody
async def regenerate_article_body(
    url: str = default_article_url,
    selected_topic: str = default_topic,
    old_article_body: str = default_article,
    current_headline: str = default_headline,
    storm: bool = False,
) -> ArticleBodyResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        storm_article = None
        if storm:
            storm_article = await storm_cache_retrieve(selected_topic, url)

        ai_service = ArticleGenerator()
        new_article_body = await ai_service.generate_article_body(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            old_article=old_article_body,
            current_headline=current_headline,
            storm_article=storm_article,
        )

        # ulozit article body do DB
        return new_article_body
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/articlebody", response_model=ArticleBodyResponse)
    async def regenerate_article_body_get(
        url: str = default_article_url,
        selected_topic: str = default_topic,
        old_article_body: str = default_article,
        current_headline: str = default_headline,
        storm: bool = False,
    ) -> ArticleBodyResponse:
        return await regenerate_article_body(
            url, selected_topic, old_article_body, current_headline, storm
        )


@router.post("/regenerate/articlebody", response_model=ArticleBodyResponse)
async def regenerate_article_body_post(
    request: Request,
) -> ArticleBodyResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article_url)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_article_body = request_body.get("old_article_body", default_article)
        current_headline = request_body.get("current_headline", default_headline)
        storm = request_body.get("storm", False)

        return await regenerate_article_body(
            url, selected_topic, old_article_body, current_headline, storm
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region tags
async def regenerate_tags(
    url: str = default_article,
    # ID z db pridat pre ukladanie
    selected_topic: str = default_topic,
    old_tags: list[str] = default_tags,
    current_headline: str = default_headline,
    current_article: str = default_article,
) -> TagsResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = ArticleGenerator()
        new_tags = await ai_service.generate_tags(
            scraped_content=scraped_article,
            selected_topic=selected_topic,
            old_tags=old_tags,
            current_headline=current_headline,
            current_article=current_article,
        )

        # ulozit tags do DB
        return new_tags
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/tags", response_model=TagsResponse)
    async def regenerate_tags_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_tags: list[str] = default_tags,
        current_headline: str = default_headline,
        current_article: str = default_article,
    ) -> TagsResponse:
        return await regenerate_tags(
            url, selected_topic, old_tags, current_headline, current_article
        )


@router.post("/regenerate/tags", response_model=TagsResponse)
async def regenerate_tags_post(
    request: Request,
) -> TagsResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_tags = request_body.get("old_tags", default_tags)
        current_headline = request_body.get("current_headline", default_headline)
        current_article = request_body.get("current_article", default_article)

        return await regenerate_tags(
            url, selected_topic, old_tags, current_headline, current_article
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region STORM Microservice
async def health_check() -> dict[str, str]:
    try:
        async with httpx.AsyncClient() as client:
            storm_host = os.getenv("STORM_HOST", "localhost")
            response = await client.get(f"http://{storm_host}:8001/health")
            if response.status_code == 200:
                return {"status": "healthy", "storm_status": response.json()}
            else:
                return {"status": "degraded", "storm_status": response.text}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def call_storm_microservice_generate(
    selected_topic: str, article_url: str
) -> None:
    storm_host = os.getenv("STORM_HOST", "localhost")
    url = f"http://{storm_host}:8001/knowledge-storm/generate?selected_topic={selected_topic}&article_url={article_url}"

    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
        response = await client.post(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Failed to get result. Status code: {response.status_code}, {response.text}"
            }


async def storm_cache_retrieve(selected_topic: str, url: str) -> str:
    cache_key = f"storm_article:{selected_topic}:{url}"
    cached_content = await FastAPICache.get_backend().get(cache_key)

    if not cached_content:
        storm_article = await call_storm_microservice_generate(selected_topic, url)
        await FastAPICache.get_backend().set(cache_key, storm_article, expire=3600)
    else:
        storm_article = cached_content
    return storm_article


# endregion

if __name__ == "__main__":
    # result = asyncio.run(health_check())
    # result = asyncio.run(call_storm_microservice_generate(default_topic, default_article_url))
    FastAPICache.init(InMemoryBackend())
    result = asyncio.run(extract_article(default_article_url, default_topic, True))

    print(result)

import httpx
from fastapi import APIRouter, HTTPException, Request

# from fastapi_cache import FastAPICache
from backend.app.core.config import settings
from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import (
    ArticleBodyResponse,
    ArticleResponse,
    EngagingTextResponse,
    HeadlineResponse,
    PerexResponse,
    TagsResponse,
)
from backend.app.utils.default_article import (
    default_article,
    default_engaging_text,
    default_headline,
    default_headlines,
    default_perex,
    default_tags,
    default_topic,
)

# from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.scraping_cache_functions import cache_or_scrape

router = APIRouter()


# region Extract article
async def extract_article(
    url: str = default_article,
    selected_topic: str = default_topic,
) -> ArticleResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        article = await ai_service.generate_article(scraped_article, selected_topic)

        article_data = {
            "url": {"url": url},
            "heading": {"heading_content": article.headlines[0]},
            "topic": {"topic_content": selected_topic},
            "perex": {"perex_content": article.perex},
            "body": {"body_content": article.article},
            "text": {"text_content": article.engaging_text},
            "tags": [{"tag_content": tag} for tag in article.tags],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.wraite.news/save_article/", json=article_data
            )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"id": response.id, "article": article}
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
async def generate_headlines(
    url: str = default_article,
    selected_topic: str = default_topic,
) -> HeadlineResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        headlines = await ai_service.generate_headlines(scraped_article, selected_topic)

        return headlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/generate/headlines", response_model=HeadlineResponse)
    async def generate_headlines_get(
        url: str = default_article,
        selected_topic: str = default_topic,
    ) -> HeadlineResponse:
        return await generate_headlines(url, selected_topic)


@router.post("/generate/headlines", response_model=HeadlineResponse)
async def generate_headlines_post(
    request: Request,
) -> HeadlineResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)

        return await generate_headlines(url, selected_topic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def regenerate_headlines(
    url: str = default_article,
    selected_topic: str = default_topic,
    old_headlines: list[str] = default_headlines,
) -> HeadlineResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        new_headlines = await ai_service.regenerate_headlines(
            scraped_article, selected_topic, old_headlines
        )

        return new_headlines
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/headlines", response_model=HeadlineResponse)
    async def regenerate_headlines_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_headlines: str = None,
    ) -> HeadlineResponse:
        return await regenerate_headlines(url, selected_topic, old_headlines)


@router.post("/regenerate/headlines", response_model=HeadlineResponse)
async def regenerate_headlines_post(
    request: Request,
) -> HeadlineResponse:
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
async def generate_engaging_text(
    url: str = default_article,
    selected_topic: str = default_topic,
    current_headline: str = default_headline,
) -> EngagingTextResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        engaging_text = await ai_service.generate_engaging_text(
            scraped_article, selected_topic, current_headline
        )

        return engaging_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/generate/engaging_text", response_model=EngagingTextResponse)
    async def generate_engaging_text_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        current_headline: str = default_headline,
    ) -> EngagingTextResponse:
        return await generate_engaging_text(url, selected_topic, current_headline)


@router.post("/generate/engaging_text", response_model=EngagingTextResponse)
async def generate_engaging_text_post(
    request: Request,
) -> EngagingTextResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        current_headline = request_body.get("current_headline", default_headline)

        return await generate_engaging_text(url, selected_topic, current_headline)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def regenerate_engaging_text(
    url: str = default_article,
    # ID z db pridat pre ukladanie
    selected_topic: str = default_topic,
    old_engaging_text: str = default_engaging_text,
    current_headline: str = default_headline,
) -> EngagingTextResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        new_engaging_text = await ai_service.regenerate_engaging_text(
            scraped_article, selected_topic, old_engaging_text, current_headline
        )

        # Ulozit engaging text do DB
        return new_engaging_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/engaging_text", response_model=EngagingTextResponse)
    async def regenerate_engaging_text_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_engaging_text: str = default_engaging_text,
        current_headline: str = default_headline,
    ) -> EngagingTextResponse:
        return await regenerate_engaging_text(
            url, selected_topic, old_engaging_text, current_headline
        )


@router.post("/regenerate/engaging_text", response_model=EngagingTextResponse)
async def regenerate_engaging_text_post(
    request: Request,
) -> EngagingTextResponse:
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


# region Perex
async def generate_perex(
    url: str = default_article,
    selected_topic: str = default_topic,
    current_headline: str = default_headline,
) -> EngagingTextResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        perex = await ai_service.generate_perex(
            scraped_article, selected_topic, current_headline
        )

        return perex
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/generate/perex", response_model=PerexResponse)
    async def generate_perex_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        current_headline: str = default_headline,
    ) -> PerexResponse:
        return await generate_perex(url, selected_topic, current_headline)


@router.post("/generate/perex", response_model=PerexResponse)
async def generate_perex_post(
    request: Request,
) -> PerexResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        current_headline = request_body.get("current_headline", default_headline)

        return await generate_perex(url, selected_topic, current_headline)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def regenerate_perex(
    url: str = default_article,
    # ID z db pridat pre ukladanie
    selected_topic: str = default_topic,
    old_perex: str = default_perex,
    current_headline: str = default_headline,
) -> EngagingTextResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        new_perex = await ai_service.regenerate_perex(
            scraped_article, selected_topic, old_perex, current_headline
        )

        # ulozit perex do DB
        return new_perex
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/perex", response_model=PerexResponse)
    async def regenerate_perex_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_perex: str = default_perex,
        current_headline: str = default_headline,
    ) -> PerexResponse:
        return await regenerate_perex(url, selected_topic, old_perex, current_headline)


@router.post("/regenerate/perex", response_model=PerexResponse)
async def regenerate_perex_post(
    request: Request,
) -> PerexResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_perex = request_body.get("old_perex", default_perex)
        current_headline = request_body.get("current_headline", default_headline)

        return await regenerate_perex(url, selected_topic, old_perex, current_headline)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region ArticleBody
async def generate_article_body(
    url: str = default_article,
    selected_topic: str = default_topic,
    current_headline: str = default_headline,
) -> ArticleBodyResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        article_body = await ai_service.generate_article_body(
            scraped_article, selected_topic, current_headline
        )

        return article_body
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/generate/articlebody", response_model=ArticleBodyResponse)
    async def generate_article_body_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        current_headline: str = default_headline,
    ) -> ArticleBodyResponse:
        return await generate_article_body(url, selected_topic, current_headline)


@router.post("/generate/articlebody", response_model=ArticleBodyResponse)
async def generate_article_body_post(
    request: Request,
) -> ArticleBodyResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        current_headline = request_body.get("current_headline", default_headline)

        return await generate_article_body(url, selected_topic, current_headline)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def regenerate_article_body(
    url: str = default_article,
    # ID z db pridat pre ukladanie
    selected_topic: str = default_topic,
    old_article_body: str = default_article,
    current_headline: str = default_headline,
) -> ArticleBodyResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        new_article_body = await ai_service.regenerate_article_body(
            scraped_article, selected_topic, old_article_body, current_headline
        )

        # ulozit article body do DB
        return new_article_body
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/regenerate/articlebody", response_model=ArticleBodyResponse)
    async def regenerate_article_body_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        old_article_body: str = default_article,
        current_headline: str = default_headline,
    ) -> ArticleBodyResponse:
        return await regenerate_article_body(
            url, selected_topic, old_article_body, current_headline
        )


@router.post("/regenerate/articlebody", response_model=ArticleBodyResponse)
async def regenerate_article_body_post(
    request: Request,
) -> ArticleBodyResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        old_article_body = request_body.get("old_article_body", default_article)
        current_headline = request_body.get("current_headline", default_headline)

        return await regenerate_article_body(
            url, selected_topic, old_article_body, current_headline
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region tags
async def generate_tags(
    url: str = default_article,
    selected_topic: str = default_topic,
    current_headline: str = default_headline,
    current_article: str = default_article,
) -> TagsResponse:
    try:
        scraped_article = await cache_or_scrape(url, default_article)

        ai_service = LiteLLMService()
        tags = await ai_service.generate_tags(
            scraped_article, selected_topic, current_headline, current_article
        )

        return tags
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if settings.ENVIRONMENT == "development":

    @router.get("/generate/tags", response_model=TagsResponse)
    async def generate_tags_get(
        url: str = default_article,
        selected_topic: str = default_topic,
        current_headline: str = default_headline,
        current_article: str = default_article,
    ) -> TagsResponse:
        return await generate_tags(
            url, selected_topic, current_headline, current_article
        )


@router.post("/generate/tags", response_model=TagsResponse)
async def generate_tags_post(
    request: Request,
) -> TagsResponse:
    try:
        request_body = await request.json()
        url = request_body.get("url", default_article)
        selected_topic = request_body.get("selected_topic", default_topic)
        current_headline = request_body.get("current_headline", default_headline)
        current_article = request_body.get("current_article", default_article)

        return await generate_tags(
            url, selected_topic, current_headline, current_article
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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

        ai_service = LiteLLMService()
        new_tags = await ai_service.regenerate_tags(
            scraped_article, selected_topic, old_tags, current_headline, current_article
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

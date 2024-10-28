from fastapi import APIRouter, HTTPException

from backend.app.api.routes.url_to_topic import articles_cache
from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import ArticleResponse
from backend.app.utils.default_article import default_article

router = APIRouter()


@router.get("/article/generate", response_model=ArticleResponse)
async def extract_article(
    url: str = default_article,
) -> ArticleResponse:
    try:
        # Temporary solution until scraper works again, change logic once it works
        scraped_article = "Article is missing"
        if url in articles_cache:
            scraped_article = articles_cache[url]
        elif url == default_article:
            scraped_article = default_article

        ai_service = LiteLLMService()
        article = ai_service.generate_article(scraped_article)

        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

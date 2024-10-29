from fastapi import APIRouter, HTTPException

from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.ai_service.response_models import TopicsResponse
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.default_article import default_article, default_article_url

router = APIRouter()

# Global cache for the scraped article
# Cache as dict will probably be necessary once, similar articles will be looked up in vector db.
articles_cache = {}


# Temporary default url for testing purposes, temporary get and post method at the same time
@router.post("/article/topics", response_model=TopicsResponse)
@router.get("/article/topics", response_model=TopicsResponse)  # Also allow GET requests
async def extract_topics(
    url: str = default_article,
) -> TopicsResponse:
    try:
        # Temporary solution until scraper works again
        if url not in articles_cache:
            if url == default_article:
                scraped_content = url
                articles_cache[default_article_url] = scraped_content
            else:
                scraped_content = await jina_scrape(url)
                articles_cache[url] = scraped_content
        else:
            scraped_content = articles_cache[url]

        ai_service = LiteLLMService()
        generated_topics = await ai_service.generate_topics(scraped_content)

        return generated_topics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

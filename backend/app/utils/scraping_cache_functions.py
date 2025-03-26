from fastapi_cache import FastAPICache

from backend.app.core.config import settings
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.services.scraping_service.playwright_scraper import scrape
from backend.app.utils.default_article import default_article


async def cache_or_scrape(
    url: str,
    default_article_url: str,
) -> str:
    if settings.SCRAPER == "jina":
        cache_key = f"article:{url}"
        default_cache_key = f"article:{default_article_url}"
        cached_content = await FastAPICache.get_backend().get(cache_key)

        if not cached_content:
            if url == default_article_url:
                scraped_article = default_article
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

    elif settings.SCRAPER == "playwright":
        cache_key = f"article:{url}"
        default_cache_key = f"article:{default_article_url}"
        cached_content = await FastAPICache.get_backend().get(cache_key)

        if not cached_content:
            if url == default_article_url:
                scraped_article = default_article
                await FastAPICache.get_backend().set(
                    default_cache_key, scraped_article, expire=3600
                )
            else:
                scraped_article = await scrape(url)
                await FastAPICache.get_backend().set(
                    cache_key, scraped_article, expire=3600
                )
        else:
            scraped_article = cached_content

    return scraped_article

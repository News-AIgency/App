from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.app.services.ai_service.litellm_service import LiteLLMService
from backend.app.services.scraping_service.jina_scraper import jina_scrape

router = APIRouter()

articles_cache = {}


class ArticleResponse(BaseModel):
    headlines: list[str]
    perex: str
    article: str


@router.get("/article_article", response_model=ArticleResponse)
async def extract_article(
    url: str = Query(
        "https://slovak.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/7516cc54-0681-4ae1"
        "-b46d-81c1f056461d/!ut/p/z1/tZRPU7MwEMY_iwePmWwg_PGYog1URIFC21wcpGixFmph8PX99IZOHcdxGurBXAiT59lsdn8JFniORZV15V"
        "PWlnWVvcj_hTDvQ8uzRyPCAEa-Dt7kOg5cZ6zxxMCz7wI7iK7Am7I7Hk0oAWpgIZdZGIaxn6bAU20Mnk44BEkCMLYOfoWg94_jO41dUO5cRrdy"
        "eepoduybGgA5-B3OXGr5ALbPDfCYm0QXoa4D0_f-r_QMC8ALYhk6jWFK6cEPRwaD0_yKBI_7OZv-rN8PgcIfgqn29wJF_jGA0r8XnHR-hUCo-U"
        "mxwCKv2m27wov6oclWqFmjsnpE2bo9BzmpdxtJY1cVqNnusu79HLqmaNfyaxnEzHODIjBtgmhWEPRAzSWySU4ewTCpSZZ9-G1eLvHiJPVsiHeh"
        "pmXW7zcA5FAMMcS8UENB1YI9VMq2DkTYY7GQhbKOForIi92VxRtOqr59Lzj-ZR9cwJMhdOTbVD6_vgomAaqrtvjX4vlfECT30XY3zs2TPEHWrv"
        "rQNZ6fZN1uks-xsfV3tI6uIvf_KEB8Zjfs7OwDaThnGA!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"
    ),
) -> ArticleResponse:
    try:
        if url not in articles_cache:
            scraped_content = await jina_scrape(url)
            articles_cache[url] = scraped_content
        else:
            scraped_content = articles_cache[url]

        ai_service = LiteLLMService()
        article_sections = ai_service.generate_article(scraped_content)

        headlines = article_sections[0] if len(article_sections) > 0 else []
        perex = (
            article_sections[1][0]
            if len(article_sections) > 1 and len(article_sections[1]) > 0
            else ""
        )
        article_content = (
            article_sections[2][0]
            if len(article_sections) > 2 and len(article_sections[2]) > 0
            else ""
        )

        return ArticleResponse(
            headlines=headlines, perex=perex, article=article_content
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

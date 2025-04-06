import asyncio

import dspy
from dspy_signatures import GenerateGraphs

from backend.app.core.config import settings
from backend.app.services.scraping_service.jina_scraper import jina_scrape
from backend.app.utils.language_enum import Language


def _configure_lm(model_name: str) -> None:
    kwargs = {
        "model": model_name,
        "api_key": settings.LITE_LLM_KEY,
        "base_url": "http://147.175.151.44/",
    }

    lm = dspy.LM(**kwargs)
    dspy.settings.configure(lm=lm, async_max_workers=8)


async def plot_gen_graph() -> None:
    scraped_article = await jina_scrape(
        "https://slovak.statistics.sk/wps/portal/ext/products/informationmessages/inf_sprava_detail/9eaafb85-7fc2-4ff4-93d4-431caff0c46d/!ut/p/z1/tVFNc4IwFPwtPXjMvIcEwWOwLWDVqVKK5NKJSJSigJKh9d83dHrpwY8emstLZnY3u2-BwxJ4Kdp8I1RelWKn3wkfvM3twHFdgyG6ExOD8VM480ePfS-yIP4NcGaLBwxe2LO3GFMDqQX8Mv8VOPC0VLXaQlKtGrElTUHyUhJRqB7qS3XcazdtmZGmPor21MO2yVSh5zATQq4ci9gy7RMqJSVDc00JNY1USIkpHaw7-TrN15DchI6v5e3i4JnDUPP5N2TkMZ_aE0Rn4lkYMD9aDOemicz8AVzQCJsCEu3DPuvDsCFu8-wDorLbzg7CP8b0EcbXmtHV5--HA2e6n6pU2aeC5X8UpP_pH6ej6UYnEGrbSVewvIla76O9Y55IIe_dGfFip2F3X92dAMM!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"
    )

    generate_graph_program = GenerateGraphs()
    generate_graph_program = dspy.asyncify(generate_graph_program)
    result = await generate_graph_program(scraped_article, Language.SLOVAK)

    with open(
        r"C:\FIIT_STU\ING_studium\TP\App\backend\app\services\ai_service\test_graph_code.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(result.graph_code)


if __name__ == "__main__":
    _configure_lm("gpt-4o-mini")
    asyncio.run(plot_gen_graph())

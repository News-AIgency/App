import aiohttp
import requests
from validators import ValidationError
from validators import url as validate_url


def check_url(url: str) -> bool:
    result = validate_url(url)

    if isinstance(result, ValidationError):
        return False

    return result


async def jina_scrape(scrape_url: str) -> str | None:

    if not check_url(scrape_url):
        raise ValueError("The argument is not a valid URL")

    url = f"https://r.jina.ai/{scrape_url}"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(url, headers=headers) as response,
        ):

            response.raise_for_status()
            return await response.text()
    except requests.RequestException as e:
        raise Exception("An error has occured during request", e)

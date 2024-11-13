import validators
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter as mc
from playwright.async_api import async_playwright
from validators import ValidationError


def check_url(url: str) -> bool:
    result = validators.url(url)

    if isinstance(result, ValidationError):
        return False
    return result


def md(soup: BeautifulSoup, **options) -> str:
    return mc(**options).convert_soup(soup)


async def scrape(url: str) -> str:
    if not check_url(url):
        raise ValueError("The argument is not a valid URL")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()

        soup = BeautifulSoup(html, "html.parser")

        # Title
        title = soup.select_one(
            "#layoutContainers > div.component-container.ibm2ColRightMain.ibmDndColumn.id-Z7_Q7I8BB1A00BL30IJKSNHCF2G15 > div > div > div > div.body-content > div.publication-detail > h1"
        )
        # Keynotes
        keynotes = soup.select_one(
            "#layoutContainers > div.component-container.ibm2ColRightMain.ibmDndColumn.id-Z7_Q7I8BB1A00BL30IJKSNHCF2G15 > div > div > div > div.body-content > div.publication-detail > div.publ-detail-item > div.publ-detail-keynotes"
        )
        # Body
        body = soup.select_one(
            "#layoutContainers > div.component-container.ibm2ColRightMain.ibmDndColumn.id-Z7_Q7I8BB1A00BL30IJKSNHCF2G15 > div > div > div > div.body-content > div.publication-detail > div.publ-detail-item > div.publ-detail-text > div.body-text"
        )

        # Convert each extracted component to markdown
        title_md = md(title) if title else "Title not found"
        keynotes_md = md(keynotes) if keynotes else "Keynotes not found"
        body_md = md(body) if body else "Body not found"

        # Combine markdown content
        result_md = (
            f"## Title\n{title_md}\n## Keynotes\n{keynotes_md}\n## Body\n{body_md}"
        )
        return result_md

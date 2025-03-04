import json
import os
import sys
import unicodedata

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from backend.app.services.ai_service.response_models import ArticleResponse


def create_response_json(
    headlines: list[str],
    engaging_text: str,
    article: str,
    tags: list[str],
    chain_of_thought: str ="N/A",
) -> ArticleResponse:
    response = {
        "chain_of_thought": chain_of_thought,
        "headlines": headlines,
        "engaging_text": engaging_text,
        "perex": engaging_text,
        "article": article,
        "tags": tags,
    }
    response = json.dumps(response)

    return ArticleResponse.model_validate_json(response)


def clean_unicode(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = text.replace("\n", " ").replace("\r", " ").strip()
    return text


def fetch_html(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    req = Request(url, headers=headers)

    with urlopen(req) as response:
        return BeautifulSoup(response.read().decode("utf-8"), "html.parser")


def pravda_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(soup.find("h1", attrs={"itemprop": "headline"}).get_text())
    ]
    engaging_text = clean_unicode(
        soup.find("p", attrs={"itemprop": "description"}).get_text()
    )
    article_body = soup.find(
        "div", attrs={"itemprop": "articleBody", "class": "article-detail-body"}
    )
    article = article_body.find_all(["p", "h2", "h3", "h4", "h5"])
    article = clean_unicode(
        "\n".join(element.get_text(strip=True) for element in article)
    )
    tags = soup.find("div", class_="article-detail-tags")
    tags = tags.find_all("a")
    tags = [clean_unicode(tag.get_text()) for tag in tags]

    return create_response_json(headlines, engaging_text, article, tags)


def sme_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(soup.find("h1", attrs={"class": "js-article-title"}).get_text())
    ]
    engaging_text = clean_unicode(soup.find("p", attrs={"class": "perex"}).get_text())
    article_body = soup.find("article", attrs={"class": "js-remp-article-data"})
    article = article_body.find_all("p")
    article = clean_unicode(
        "\n".join(element.get_text(strip=True) for element in article)
    )
    tags = ["N/A"]

    return create_response_json(headlines, engaging_text, article, tags)


def dennikn_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(soup.find("h1", attrs={"class": "n3_single_title"}).get_text())
    ]
    engaging_text = clean_unicode(
        soup.find("div", attrs={"class": "entry-content"}).find("p").get_text()
    )
    article_body = soup.find("div", attrs={"class": "entry-content"})
    article = article_body.find_all("p")
    article = clean_unicode(
        "\n".join(element.get_text(strip=True) for element in article)
    )
    tags = ["N/A"]

    return create_response_json(headlines, engaging_text, article, tags)


def trend_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(
            soup.find(
                "h1", attrs={"class": "h", "data-don": "article_title"}
            ).get_text()
        )
    ]
    engaging_text = soup.find(
        "p", attrs={"class": "article-perex", "data-don": "article_perex"}
    )
    engaging_text = "".join(engaging_text.find_all(text=True, recursive=False)).strip()
    article_body = soup.find(
        "div", attrs={"data-don": "article_body", "class": "article-body"}
    )
    article = article_body.find_all("p")
    article = clean_unicode(
        "\n".join(element.get_text(strip=True) for element in article)
    )
    tags = soup.find(
        "ul", attrs={"class": "article-tags", "data-itm": "related_topics"}
    )
    tags = tags.find_all("a")
    tags = [clean_unicode(tag.get_text()) for tag in tags]

    return create_response_json(headlines, engaging_text, article, tags)


def teraz_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(soup.find("h1", attrs={"class": "articleTitle"}).get_text())
    ]
    engaging_text = clean_unicode(
        soup.find("p", attrs={"class": "articlePerex"}).get_text()
    )
    article_body = soup.find("div", attrs={"class": "articleMain"})
    article = article_body.find("div").get_text()
    article = article.replace("\n\r\n", " ").strip()
    tags = ["N/A"]

    return create_response_json(headlines, engaging_text, article, tags)


def forbes_to_article_response(soup: BeautifulSoup) -> ArticleResponse:
    headlines = [
        clean_unicode(soup.find("h1", attrs={"class": "h3-noto heading"}).get_text())
    ]
    engaging_text = clean_unicode(
        soup.find("div", attrs={"class": "gutenberg-content"}).find("p").get_text()
    )
    article_body = soup.find("div", attrs={"class": "gutenberg-content"})
    article = article_body.find_all("p")
    article = clean_unicode(
        "\n".join(element.get_text(strip=True) for element in article)
    )
    tags = soup.find("a", attrs={"class": "term__name"})
    tags = clean_unicode(tags.find("h6").get_text()) if tags else ["N/A"]

    return create_response_json(headlines, engaging_text, article, tags)


def check_origin_url(url: str) -> None:
    parsed_url = urlparse(url)
    soup = fetch_html(url)

    if parsed_url.hostname in ["uzitocna.pravda.sk", "ekonomika.pravda.sk"]:
        print(pravda_to_article_response(soup))
    elif parsed_url.hostname in ["index.sme.sk"]:
        print(sme_to_article_response(soup))
    elif parsed_url.hostname in ["e.dennikn.sk"]:
        print(dennikn_to_article_response(soup))
    elif parsed_url.hostname in ["www.trend.sk"]:
        print(trend_to_article_response(soup))
    elif parsed_url.hostname in ["www.teraz.sk"]:
        print(teraz_to_article_response(soup))
    elif parsed_url.hostname in ["www.forbes.sk"]:
        print(forbes_to_article_response(soup))


if __name__ == "__main__":
    check_origin_url(
        "https://www.forbes.sk/slovenska-ekonomika-rastla-o-18-percenta-jej-buducnost-zavisi-od-troch-faktorov/"
    )

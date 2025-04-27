import re

from backend.app.utils.default_article import default_storm_article


def extract_reference_urls(article_text: str) -> list[str]:
    pattern = r"\[\d+\]\((https?://[^\)]+)\)"
    seen = set()
    ordered_urls = []
    for url in re.findall(pattern, article_text):
        if url not in seen:
            seen.add(url)
            ordered_urls.append(url)
    return ordered_urls


if __name__ == "__main__":
    print(extract_reference_urls(default_storm_article))

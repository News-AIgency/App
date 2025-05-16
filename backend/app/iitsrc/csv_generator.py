import asyncio
import csv
import random

import pandas as pd

from backend.app.iitsrc.article_response_converter import check_origin_url
from backend.app.iitsrc.dspy_llm_judge import llm_compare_strings
from backend.app.services.ai_service.article_generator import ArticleGenerator
from backend.app.services.scraping_service.jina_scraper import jina_scrape

def generate_original_article_csv() -> None:
    file_path = "articles.xlsx"
    output_csv = "original_articles.csv"

    xls = pd.ExcelFile(file_path)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # Write header
        writer.writerow(["News Site", "Headline", "Perex", "Article", "Tags"])

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(
                xls, sheet_name=sheet_name, usecols=[0]
            )  # Read only the first column - news site url

            for url in df.iloc[:, 0].tolist():
                article_response = check_origin_url(url)

                headline = (
                    ", ".join(article_response.headlines)
                    if article_response.headlines
                    else ""
                )
                perex = article_response.perex or ""
                article = article_response.article or ""
                tags = ", ".join(article_response.tags) if article_response.tags else ""

                # Write to CSV
                writer.writerow([sheet_name, headline, perex, article, tags])

async def retry_api_call(api_func, *args, retries=3, delay=2, **kwargs):
    for attempt in range(retries):
        try:
            return await api_func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise


async def generate_generated_article_csv() -> None:
    file_path = "articles.xlsx"
    output_csv = "generated_articles.csv"

    llm_service = ArticleGenerator()
    xls = pd.ExcelFile(file_path)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["News Site", "Headline", "Perex", "Article", "Tags"])

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, usecols=[1])

            for url in df.iloc[:, 0].tolist():
                try:
                    print(f"Processing: {url}")

                    scraped_content = await retry_api_call(jina_scrape, url)

                    topics_response = await retry_api_call(
                        llm_service.generate_topics,
                        scraped_content=scraped_content,
                    )
                    selected_topic = random.choice(topics_response.topics)

                    headline_response = await retry_api_call(
                        llm_service.generate_headlines,
                        scraped_content=scraped_content,
                        selected_topic=selected_topic,
                    )
                    print("Headline complete")

                    perex_response = await retry_api_call(
                        llm_service.generate_perex,
                        scraped_content=scraped_content,
                        selected_topic=selected_topic,
                        current_headline=headline_response.headlines[0],
                    )
                    print("Perex complete")

                    article_response = await retry_api_call(
                        llm_service.generate_article_body,
                        scraped_content=scraped_content,
                        selected_topic=selected_topic,
                        current_headline=headline_response.headlines[0],
                    )
                    print("Article complete")

                    tags_response = await retry_api_call(
                        llm_service.generate_tags,
                        scraped_content=scraped_content,
                        selected_topic=selected_topic,
                        current_headline=headline_response.headlines[0],
                        current_article=article_response.article,
                    )
                    print("Tags complete")

                    headline = random.choice(headline_response.headlines)
                    perex = perex_response.perex
                    article = article_response.article
                    tags = tags_response.tags.lower()

                    writer.writerow([sheet_name, headline, perex, article, tags])
                    print("VIBAVENE OK ")

                    await asyncio.sleep(1.5)  # delay to reduce rate-limiting risk

                except Exception as e:
                    print(f"Failed to process {url}: {e}")
                    continue

async def generate_llm_as_judge_csv() -> None:
    original_articles = pd.read_csv("original_articles.csv", delimiter=";")
    generated_articles = pd.read_csv("generated_articles.csv", delimiter=";")

    original_headline_section = original_articles["Headline"]
    generated_headline_section = generated_articles["Headline"]

    original_perex_section = original_articles["Perex"]
    generated_perex_section = generated_articles["Perex"]

    original_article_section = original_articles["Article"]
    generated_article_section = generated_articles["Article"]

    scores = []
    for (
        original_headline,
        generated_headline,
        original_perex,
        generated_perex,
        original_article,
        generated_article,
    ) in zip(
        original_headline_section,
        generated_headline_section,
        original_perex_section,
        generated_perex_section,
        original_article_section,
        generated_article_section,
    ):
        headline_score = await llm_compare_strings(
            original_headline, generated_headline
        )
        perex_score = await llm_compare_strings(original_perex, generated_perex)
        article_score = await llm_compare_strings(original_article, generated_article)

        scores.append([headline_score, perex_score, article_score])

    scores_df = pd.DataFrame(scores, columns=["Headline", "Perex", "Article"])
    scores_df.to_csv("llm_as_judge_scores.csv", index=False)
    await asyncio.sleep(1.5)  # delay to reduce rate-limiting risk


if __name__ == "__main__":
    # generate_original_article_csv()
    # asyncio.run(generate_generated_article_csv())
    asyncio.run(generate_llm_as_judge_csv())

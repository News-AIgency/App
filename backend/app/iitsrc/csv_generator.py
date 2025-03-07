import asyncio
import csv
import random

import pandas as pd

from backend.app.iitsrc.article_response_converter import check_origin_url
from backend.app.iitsrc.dspy_llm_judge import llm_compare_strings
from backend.app.services.ai_service.litellm_service import LiteLLMService

# from backend.app.services.ai_service.storm_agent.STORM_service import run_storm
from backend.app.services.scraping_service.jina_scraper import jina_scrape


def generate_original_article_csv() -> None:
    file_path = "articles.xlsx"
    output_csv = "original_articles.csv"

    xls = pd.ExcelFile(file_path)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # Write header
        writer.writerow(["News Site", "Headline", "Engaging Text", "Article", "Tags"])

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
                engaging_text = article_response.engaging_text or ""
                article = article_response.article or ""
                tags = ", ".join(article_response.tags) if article_response.tags else ""

                # Write to CSV
                writer.writerow([sheet_name, headline, engaging_text, article, tags])


async def generate_generated_article_csv(storm: bool = False) -> None:
    file_path = "articles.xlsx"
    output_csv = "generated_articles_storm.csv" if storm else "generated_articles.csv"

    llm_service = LiteLLMService()
    xls = pd.ExcelFile(file_path)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["News Site", "Headline", "Engaging Text", "Article", "Tags"])

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(
                xls, sheet_name=sheet_name, usecols=[1]
            )  # Read only the second column - SUSR

            for url in df.iloc[:, 0].tolist():

                scraped_content = await jina_scrape(url)
                print(url)
                topics_response = await llm_service.generate_topics(
                    scraped_content=scraped_content
                )
                selected_topic = random.choice(topics_response.topics)

                # Generate components separately
                headline_response = await llm_service.generate_headlines(
                    scraped_content=scraped_content, selected_topic=selected_topic
                )
                print("headline complete")

                """
                                if storm:
                    storm_article = run_storm(selected_topic, url)
                    print("storm article complete")

                    engaging_text_response = (
                        await llm_service.storm_generate_engaging_text(
                            scraped_content=scraped_content,
                            storm_article=storm_article,
                            selected_topic=selected_topic,
                            current_headline=headline_response.headlines[0],
                        )
                    )
                    print("engaging text complete")

                    article_response = await llm_service.storm_generate_article_body(
                        scraped_content=scraped_content,
                        storm_article=storm_article,
                        selected_topic=selected_topic,
                        current_headline=headline_response.headlines[0],
                    )
                    print("article complete")
                else:
                """

                engaging_text_response = await llm_service.generate_engaging_text(
                    scraped_content=scraped_content,
                    selected_topic=selected_topic,
                    current_headline=headline_response.headlines[0],
                )
                print("engaging text complete")
                article_response = await llm_service.generate_article_body(
                    scraped_content=scraped_content,
                    selected_topic=selected_topic,
                    current_headline=headline_response.headlines[0],
                )
                print("article complete")

                tags_response = await llm_service.generate_tags(
                    scraped_content=scraped_content,
                    selected_topic=selected_topic,
                    current_headline=headline_response.headlines[0],
                    current_article=article_response.article,
                )
                print("tags complete")

                # Extract fields
                headline = random.choice(headline_response.headlines)
                engaging_text = engaging_text_response.engaging_text
                article = article_response.article
                tags = tags_response.tags[0].lower()

                # Write to CSV
                writer.writerow([sheet_name, headline, engaging_text, article, tags])

                print("Done")


async def generate_llm_as_judge_csv() -> None:
    original_articles = pd.read_csv("original_articles.csv", delimiter=";")
    generated_articles = pd.read_csv("generated_articles.csv", delimiter=";")

    original_article_section = original_articles["Article"]
    generated_article_section = generated_articles["Article"]

    scores = []
    print(original_article_section)
    for original_article, generated_article in zip(
        original_article_section, generated_article_section
    ):
        score = await llm_compare_strings(original_article, generated_article)
        scores.append(score)

    scores_df = pd.DataFrame(scores, columns=["LLM as judge score"])
    scores_df.to_csv("llm_as_judge_scores.csv", index=False)


if __name__ == "__main__":
    # generate_original_article_csv()
    # asyncio.run(generate_generated_article_csv())
    # asyncio.run(generate_generated_article_csv(True))
    asyncio.run(generate_llm_as_judge_csv())

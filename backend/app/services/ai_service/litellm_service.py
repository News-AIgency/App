import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import asyncio

import dspy
from litellm import acompletion

from backend.app.core.config import settings
from backend.app.services.ai_service.dspy_signatures import (
    GenerateArticle,
    GenerateArticleBody,
    GenerateEngagingText,
    GenerateHeadlines,
    GeneratePerex,
    GenerateTags,
    GenerateTopics,
    RegenerateArticleBody,
    RegenerateEngagingText,
    RegenerateHeadlines,
    RegeneratePerex,
    RegenerateTags,
    StormGenerateArticle,
    StormGenerateArticleBody,
    StormGenerateEngagingText,
    StormGeneratePerex,
)
from backend.app.services.ai_service.response_models import (
    ArticleBodyResponse,
    ArticleResponse,
    EngagingTextResponse,
    HeadlineResponse,
    PerexResponse,
    TagsResponse,
    TestLiteLLMPoem,
    TopicsResponse,
)
from backend.app.utils.default_article import (
    default_article,
    default_topic,
)
from backend.app.utils.language_enum import Language


class LiteLLMService:

    def __init__(self) -> None:
        self.api_key = settings.LITE_LLM_KEY
        self.litellm_url = "http://147.175.151.44/"
        self.gpt_4o_mini_model = "gpt-4o-mini"
        self.o1_mini_model = "o1_mini"

    async def test_litellm(self) -> TestLiteLLMPoem:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=TestLiteLLMPoem,
            messages=[
                {
                    "role": "user",
                    "content": "this is a test request, write a short poem",
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return TestLiteLLMPoem.model_validate_json(response.choices[0].message.content)

    async def generate_topics(
        self,
        scraped_content: str | None,
        topics_count: int = 5,
        language: Language = Language.SLOVAK,
    ) -> TopicsResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_topics_program = GenerateTopics()
        generate_topics_program = dspy.asyncify(generate_topics_program)
        generated_topics = await generate_topics_program(
            topics_count=topics_count,
            scraped_content=scraped_content,
            language=language,
        )

        return TopicsResponse(topics=generated_topics.topics.split("\n"))

    async def generate_article(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        headlines_count: int = 3,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_article_program = GenerateArticle()
        generate_article_program = dspy.asyncify(generate_article_program)
        generated_article = await generate_article_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            headlines_count=headlines_count,
            tag_count=tag_count,
            language=language,
        )

        return ArticleResponse(
            headlines=generated_article.headlines.split("\n"),
            perex=generated_article.perex,
            engaging_text=generated_article.engaging_text,
            article=generated_article.article,
            tags=generated_article.tags.split("\n"),
        )

    async def storm_generate_article(
        self,
        scraped_content: str | None,
        storm_article: str | None,
        selected_topic: str | None,
        headlines_count: int = 3,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_article_program = StormGenerateArticle()
        generate_article_program = dspy.asyncify(generate_article_program)
        generated_article = await generate_article_program(
            scraped_content=scraped_content,
            storm_article=storm_article,
            selected_topic=selected_topic,
            headlines_count=headlines_count,
            tag_count=tag_count,
            language=language,
        )

        return ArticleResponse.model_validate_json(generated_article.article)

    async def generate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> HeadlineResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_headlines_program = GenerateHeadlines()
        generate_headlines_program = dspy.asyncify(generate_headlines_program)
        generated_headlines = await generate_headlines_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            headlines_count=headlines_count,
            language=language,
        )

        return HeadlineResponse(headlines=generated_headlines.headlines.split("\n"))

    async def regenerate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_headlines: list[str],
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> HeadlineResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        regenerate_headlines_program = RegenerateHeadlines()
        regenerate_headlines_program = dspy.asyncify(regenerate_headlines_program)
        generated_headlines = await regenerate_headlines_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_headlines=old_headlines,
            headlines_count=headlines_count,
            language=language,
        )

        return HeadlineResponse(headlines=generated_headlines.headlines.split("\n"))

    async def generate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_engaging_text_program = GenerateEngagingText()
        generate_engaging_text_program = dspy.asyncify(generate_engaging_text_program)
        generated_engaging_text = await generate_engaging_text_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return EngagingTextResponse(engaging_text=generated_engaging_text.engaging_text)

    async def regenerate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_engaging_text: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        regenerate_engaging_text_program = RegenerateEngagingText()
        regenerate_engaging_text_program = dspy.asyncify(
            regenerate_engaging_text_program
        )
        generated_engaging_text = await regenerate_engaging_text_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_engaging_text=old_engaging_text,
            current_headline=current_headline,
            language=language,
        )

        return EngagingTextResponse(engaging_text=generated_engaging_text.engaging_text)

    async def storm_generate_engaging_text(
        self,
        scraped_content: str | None,
        storm_article: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_engaging_text_program = StormGenerateEngagingText()
        generate_engaging_text_program = dspy.asyncify(generate_engaging_text_program)
        generated_engaging_text = await generate_engaging_text_program(
            scraped_content=scraped_content,
            storm_article=storm_article,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return EngagingTextResponse(engaging_text=generated_engaging_text.engaging_text)

    async def generate_perex(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_perex_program = GeneratePerex()
        generate_perex_program = dspy.asyncify(generate_perex_program)
        generated_perex = await generate_perex_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return PerexResponse(perex=generated_perex.perex)

    async def regenerate_perex(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_perex: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        regenerate_perex_program = RegeneratePerex()
        regenerate_perex_program = dspy.asyncify(regenerate_perex_program)
        generated_perex = await regenerate_perex_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_perex=old_perex,
            current_headline=current_headline,
            language=language,
        )

        return PerexResponse(perex=generated_perex.perex)

    async def storm_generate_perex(
        self,
        scraped_content: str | None,
        storm_article: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_perex_program = StormGeneratePerex()
        generate_perex_program = dspy.asyncify(generate_perex_program)
        generated_perex = await generate_perex_program(
            scraped_content=scraped_content,
            storm_article=storm_article,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return PerexResponse(perex=generated_perex.perex)

    async def generate_article_body(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        lm = dspy.LM(
            "openai/o1-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
            temperature=1.0,
            max_tokens=5000,
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_article_body_program = GenerateArticleBody()
        generate_article_body_program = dspy.asyncify(generate_article_body_program)
        generated_article = await generate_article_body_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return ArticleBodyResponse(article=generated_article.article)

    async def regenerate_article_body(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_article: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        lm = dspy.LM(
            "openai/o1-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
            temperature=1.0,
            max_tokens=5000,
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        regenerate_article_body_program = RegenerateArticleBody()
        regenerate_article_body_program = dspy.asyncify(regenerate_article_body_program)
        generated_article = await regenerate_article_body_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_article=old_article,
            current_headline=current_headline,
            language=language,
        )

        return ArticleBodyResponse(article=generated_article.article)

    async def storm_generate_article_body(
        self,
        scraped_content: str | None,
        storm_article: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        lm = dspy.LM(
            "openai/o1-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
            temperature=1.0,
            max_tokens=5000,
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_article_body_program = StormGenerateArticleBody()
        generate_article_body_program = dspy.asyncify(generate_article_body_program)
        generated_article = await generate_article_body_program(
            scraped_content=scraped_content,
            storm_article=storm_article,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )

        return ArticleBodyResponse(article=generated_article.article)

    async def generate_tags(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        current_article: str | None,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> TagsResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        generate_tags_program = GenerateTags()
        generate_tags_program = dspy.asyncify(generate_tags_program)
        generated_tags = await generate_tags_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            current_article=current_article,
            tag_count=tag_count,
            language=language,
        )

        return TagsResponse(tags=generated_tags.tags.split("\n"))

    async def regenerate_tags(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_tags: list[str] | None,
        current_headline: str | None,
        current_article: str | None,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> TagsResponse:
        lm = dspy.LM(
            "openai/gpt-4o-mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
        )
        dspy.settings.configure(lm=lm, async_max_workers=8)
        regenerate_tags_program = RegenerateTags()
        regenerate_tags_program = dspy.asyncify(regenerate_tags_program)
        generated_tags = await regenerate_tags_program(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_tags=old_tags,
            current_headline=current_headline,
            current_article=current_article,
            tag_count=tag_count,
            language=language,
        )

        return TagsResponse(tags=generated_tags.tags.split("\n"))


if __name__ == "__main__":
    LM = LiteLLMService()
    asyncio.run(
        LM.generate_article(
            scraped_content=default_article, selected_topic=default_topic
        )
    )

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import asyncio

import dspy

from backend.app.core.config import settings
from backend.app.services.ai_service.dspy_signatures import (
    GenerateArticleBody,
    GenerateEngagingText,
    GenerateGraphs,
    GenerateHeadlines,
    GeneratePerex,
    GenerateTags,
    GenerateTopics,
    RegenerateArticleBody,
    RegenerateEngagingText,
    RegenerateHeadlines,
    RegeneratePerex,
    RegenerateTags,
    StormGenerateArticleBody,
    StormGenerateEngagingText,
    StormGeneratePerex,
)
from backend.app.services.ai_service.response_models import (
    ArticleBodyResponse,
    ArticleResponse,
    EngagingTextResponse,
    GraphResponse,
    HeadlineResponse,
    PerexResponse,
    TagsResponse,
    TopicsResponse,
)
from backend.app.utils.default_article import (
    default_article,
    default_topic,
)
from backend.app.utils.language_enum import Language


class ArticleGenerator:

    def __init__(self) -> None:
        self.api_key = settings.LITE_LLM_KEY
        self.litellm_url = "http://147.175.151.44/"
        self.models = {
            "gpt-4o-mini": "gpt-4o-mini",
            "o1-mini": "o1-mini",
        }

    def _configure_lm(self, model_name: str) -> None:
        kwargs = {
            "model": model_name,
            "api_key": self.api_key,
            "base_url": self.litellm_url,
        }
        if model_name.startswith("o1-"):
            kwargs["temperature"] = 1.0
            kwargs["max_tokens"] = 5000

        lm = dspy.LM(**kwargs)
        dspy.settings.configure(lm=lm, async_max_workers=8)

    async def generate_topics(
        self,
        scraped_content: str | None,
        topics_count: int = 5,
        language: Language = Language.SLOVAK,
    ) -> TopicsResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

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
        storm_article: str | None = None,
        headlines_count: int = 3,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        headlines = (
            await self.generate_headlines(
                scraped_content=scraped_content,
                selected_topic=selected_topic,
                headlines_count=headlines_count,
                language=language,
            ),
        )
        perex = (
            await self.generate_perex(
                scraped_content=scraped_content,
                selected_topic=selected_topic,
                storm_article=storm_article,
                current_headline=None,
                language=language,
            ),
        )
        engaging_text = (
            await self.generate_engaging_text(
                scraped_content=scraped_content,
                selected_topic=selected_topic,
                storm_article=storm_article,
                current_headline=None,
                language=language,
            ),
        )
        article = (
            await self.generate_article_body(
                scraped_content=scraped_content,
                selected_topic=selected_topic,
                storm_article=storm_article,
                current_headline=None,
                language=language,
            ),
        )
        tags = (
            await self.generate_tags(
                scraped_content=scraped_content,
                selected_topic=selected_topic,
                current_headline=None,
                current_article=article[0].article,
                tag_count=tag_count,
                language=language,
            ),
        )
        graph_metadata = (
            await self.generate_graph(
                scraped_content=scraped_content,
                language=language,
            ),
        )

        return ArticleResponse(
            headlines=headlines[0].headlines,
            perex=perex[0].perex,
            engaging_text=engaging_text[0].engaging_text,
            article=article[0].article,
            tags=tags[0].tags,
            graph_metadata=graph_metadata[0],
        )

    async def generate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_headlines: list[str] | None = None,
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> HeadlineResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        generator = RegenerateHeadlines if old_headlines else GenerateHeadlines
        generate_headlines_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "selected_topic": selected_topic,
            "headlines_count": headlines_count,
            "language": language,
        }
        if old_headlines:
            kwargs["old_headlines"] = old_headlines

        generated_headlines = await generate_headlines_program(**kwargs)

        return HeadlineResponse(headlines=generated_headlines.headlines.split("\n"))

    async def generate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        storm_article: str | None = None,
        old_engaging_text: str | None = None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        if storm_article and old_engaging_text:
            raise NotImplementedError(
                "STORM regenerate engaging text is not implemented yet."
            )
        elif storm_article:
            generator = StormGenerateEngagingText
        elif old_engaging_text:
            generator = RegenerateEngagingText
        else:
            generator = GenerateEngagingText

        generate_engaging_text_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "selected_topic": selected_topic,
            "current_headline": current_headline,
            "language": language,
        }
        if storm_article:
            kwargs["storm_article"] = storm_article
        if old_engaging_text:
            kwargs["old_engaging_text"] = old_engaging_text

        generated_engaging_text = await generate_engaging_text_program(**kwargs)

        return EngagingTextResponse(engaging_text=generated_engaging_text.engaging_text)

    async def generate_perex(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        storm_article: str | None = None,
        old_perex: str | None = None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        if storm_article and old_perex:
            raise NotImplementedError("STORM regenerate perex is not implemented yet.")
        elif storm_article:
            generator = StormGeneratePerex
        elif old_perex:
            generator = RegeneratePerex
        else:
            generator = GeneratePerex

        generate_perex_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "selected_topic": selected_topic,
            "current_headline": current_headline,
            "language": language,
        }
        if storm_article:
            kwargs["storm_article"] = storm_article
        if old_perex:
            kwargs["old_perex"] = old_perex

        generated_perex = await generate_perex_program(**kwargs)

        return PerexResponse(perex=generated_perex.perex)

    async def generate_article_body(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        storm_article: str | None = None,
        old_article: str | None = None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        self._configure_lm(self.models.get("o1-mini"))

        if storm_article and old_article:
            raise NotImplementedError("STORM regenerate body is not implemented yet.")
        elif storm_article:
            generator = StormGenerateArticleBody
        elif old_article:
            generator = RegenerateArticleBody
        else:
            generator = GenerateArticleBody

        generate_article_body_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "selected_topic": selected_topic,
            "current_headline": current_headline,
            "language": language,
        }
        if storm_article:
            kwargs["storm_article"] = storm_article
        if old_article:
            kwargs["old_article"] = old_article

        generated_article = await generate_article_body_program(**kwargs)

        return ArticleBodyResponse(article=generated_article.article)

    async def generate_tags(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        current_article: str | None,
        old_tags: list[str] | None = None,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> TagsResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        generator = RegenerateTags if old_tags else GenerateTags

        generate_tags_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "selected_topic": selected_topic,
            "current_headline": current_headline,
            "current_article": current_article,
            "tag_count": tag_count,
            "language": language,
        }
        if old_tags:
            kwargs["old_tags"] = old_tags

        generated_tags = await generate_tags_program(**kwargs)

        return TagsResponse(tags=generated_tags.tags.split("\n"))

    async def generate_graph(
        self,
        scraped_content: str | None,
        language: Language = Language.SLOVAK,
    ) -> GraphResponse:
        self._configure_lm(self.models.get("gpt-4o-mini"))

        generator = GenerateGraphs()

        generate_graphs_program = dspy.asyncify(generator())
        kwargs = {
            "scraped_content": scraped_content,
            "language": language,
        }

        graph_response = await generate_graphs_program(**kwargs)

        return GraphResponse(
            gen_graph=graph_response.gen_graph,
            graph_type=graph_response.graph_type,
            graph_data=graph_response.graph_data,
        )


if __name__ == "__main__":
    LM = ArticleGenerator()
    asyncio.run(
        LM.generate_article(
            scraped_content=default_article, selected_topic=default_topic
        )
    )

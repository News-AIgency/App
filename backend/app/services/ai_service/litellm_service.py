import instructor
from litellm import acompletion

from backend.app.core.config import settings
from backend.app.services.ai_service.response_models import (
    ArticleResponse,
    TestLiteLLMPoem,
    TopicsResponse,
)
from backend.app.utils.language_enum import Language


class LiteLLMService:

    def __init__(self) -> None:
        self.api_key = settings.LITE_LLM_KEY
        self.litellm_url = "http://147.175.151.44/"
        self.model = "gpt-4o-mini"

        self.client = instructor.from_litellm(acompletion)

    async def test_litellm(self) -> TestLiteLLMPoem:
        response = await self.client.chat.completions.create(
            model=self.model,
            response_model=TestLiteLLMPoem,
            messages=[
                {
                    "role": "user",
                    "content": "this is a test request, write a short poem",
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

    async def generate_topics(
        self,
        scraped_content: str | None,
        topics_count: int = 5,
        language: Language = Language.SLOVAK,
    ) -> TopicsResponse:
        response = await self.client.chat.completions.create(
            model=self.model,
            response_model=TopicsResponse,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate list of {topics_count} topics based on this scraped news article: {scraped_content}. "
                    f"No numbering, no introductory text, just topics. "
                    f"The result should not have any characters representing bullet points. "
                    f"The topics should be in the {language} language as the news article. "
                    f"The news report should be factual as well as neutral.",
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

    async def generate_article(
        self,
        scraped_content: str | None,
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        response = await self.client.completions.create(
            model=self.model,
            response_model=ArticleResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate three sections based on this scraped news article: {scraped_content}. "
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language as the news article. Sections will follow the rules below: "
                        f"1. Headlines: Generate {headlines_count} headlines that interpret the news in a human-readable way. Headlines should "
                        f"not be too long to avoid truncation."
                        f"2. Perex: A short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence "
                        f"should be interesting, but not too long to avoid truncation. "
                        f"3. Article: Write a detailed news story that includes as much information as possible found in the scraped content, "
                        f"covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? "
                        f"Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. "
                        f"Stick to factual reporting without adding commentary or opinions. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

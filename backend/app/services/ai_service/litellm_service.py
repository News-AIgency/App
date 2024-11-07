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
                    f"Each topic should start with capital letter."
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
        selected_topic: str | None,
        headlines_count: int = 3,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        response = await self.client.completions.create(
            model=self.model,
            response_model=ArticleResponse,
            temperature=0.3,
            top_p = 0.4,
            presence_penalty=-0.3,
            frequency_penalty=0.6,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate 5 sections based on this scraped news article: {scraped_content}, and the selected topic: {selected_topic}. "
                        f"The result should not have any characters representing bullet points. Do not create any new information and do not "
                        f"use any information that is not present in the given news article. Do not exaggerate! The generated fields "
                        f"should not have any resemblance to a boulevard article. "
                        f"All generated text should be in the {language} language. Sections will follow the rules below: "
                        f"1. Headlines: Generate {headlines_count} headlines that interpret the news in a human-readable way. Headlines should "
                        f"be between 70 and 110 characters, including spaces. All headlines should start with a capital letter."
                        f"2. Engaging text: Generate an engaging text that will hook the reader. Engaging text should not be longer than 240 "
                        f"characters including spaces. Engaging text will not be a part of the actual news article, but still should relate to the "
                        f"headline and compliment it."
                        f"3. Perex: A short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence "
                        f"should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex will be part of the news article"
                        f"4. Article: Write a detailed news story that includes as much information as possible found in the given article, "
                        f"covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? "
                        f"Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. "
                        f"Use numbers that are available in the given article - do not make up numbers. "
                        f"It is extremely important that you adhere to the facts and numbers given in the article."
                        f"Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance "
                        f"to a boulevard article."
                        f"The article should be split into atleast 3 paragraphs with '\n' symbols."
                        f"5. Tags: Generate {tag_count} tags, starting with a '#'. Tags should relate to the article so readers can find it easily "
                        f"and should be all capital letters."
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

    async def regenerate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_headlines: str | None,
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
                        f"Generate {headlines_count} new headlines that interpret the news in a human-readable way, based on this "
                        f"scraped news article: {scraped_content}, and the selected topic: {selected_topic}. Headlines should "
                        f"be between 70 and 110 characters, including spaces. All headlines should start with a capital letter."
                        f"Here are the old headlines: {old_headlines}. Do not repeat them, and they should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the headlines field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

    async def regenerate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_engaging_text: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        response = await self.client.completions.create(
            model=self.model,
            response_model=ArticleResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate an engaging text that will hook the reader, based on this "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"Engaging text should not be longer than 240 characters including spaces. "
                        f"Engaging text will not be a part of the actual news article, but still should relate to the "
                        f"headline and compliment it. Do not repeat them, and they should not be similiar."
                        f"Here is the old engaging text: {old_engaging_text}. Do not repeat it, and it should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the engaging text field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response

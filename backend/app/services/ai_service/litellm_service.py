from litellm import acompletion

from backend.app.core.config import settings
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
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=TopicsResponse,
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

        return TopicsResponse.model_validate_json(response.choices[0].message.content)

    async def generate_article(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        headlines_count: int = 3,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> ArticleResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=ArticleResponse,
            temperature=0.3,
            top_p=0.4,
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

        return ArticleResponse.model_validate_json(response.choices[0].message.content)

    async def generate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> HeadlineResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=HeadlineResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate {headlines_count} new headlines that interpret the news in a human-readable way, based on this "
                        f"scraped news article: {scraped_content}, and the selected topic: {selected_topic}. Headlines should "
                        f"be between 70 and 110 characters, including spaces. All headlines should start with a capital letter, meaning the first "
                        f"word will start with a capital letter and the rest will be lower case. "
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the headlines field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return HeadlineResponse.model_validate_json(response.choices[0].message.content)

    async def regenerate_headlines(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_headlines: str | None,
        headlines_count: int = 3,
        language: Language = Language.SLOVAK,
    ) -> HeadlineResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=HeadlineResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate {headlines_count} new headlines that interpret the news in a human-readable way, based on this "
                        f"scraped news article: {scraped_content}, and the selected topic: {selected_topic}. Headlines should "
                        f"be between 70 and 110 characters, including spaces. All headlines should start with a capital letter, meaning the first "
                        f"word will start with a capital letter and the rest will be lower case. "
                        f"Here are the old headlines: {old_headlines}. Do not repeat them, and they should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the headlines field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return HeadlineResponse.model_validate_json(response.choices[0].message.content)

    async def generate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=EngagingTextResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate an engaging text that will hook the reader, based on this "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"Engaging text should not be longer than 240 characters including spaces. "
                        f"Engaging text will not be a part of the actual news article, but still should relate to the "
                        f"headline and compliment it. "
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the engaging text field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return EngagingTextResponse.model_validate_json(
            response.choices[0].message.content
        )

    async def regenerate_engaging_text(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_engaging_text: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> EngagingTextResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=EngagingTextResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate an engaging text that will hook the reader, based on this "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"Engaging text should not be longer than 240 characters including spaces. "
                        f"Engaging text will not be a part of the actual news article, but still should relate to the "
                        f"headline and compliment it. "
                        f"Here is the old engaging text: {old_engaging_text}. Do not repeat it, and it should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. Fill in only the engaging text field, the other fields should remain null. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return EngagingTextResponse.model_validate_json(
            response.choices[0].message.content
        )

    async def generate_perex(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=PerexResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate a perex: a short, engaging text of 140-160 characters that complements the headlines and attracts readers. "
                        f"The first sentence should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex "
                        f"will be part of the news article. Generate it based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return PerexResponse.model_validate_json(response.choices[0].message.content)

    async def regenerate_perex(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_perex: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> PerexResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=PerexResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate a perex: a short, engaging text of 140-160 characters that complements the headlines and attracts readers. "
                        f"The first sentence should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex "
                        f"will be part of the news article. Generate it based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"Here is the old perex: {old_perex}. Do not repeat it, and it should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return PerexResponse.model_validate_json(response.choices[0].message.content)

    async def generate_article_body(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        response = await acompletion(
            model=self.o1_mini_model,
            response_format=ArticleBodyResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate an article: a detailed news story that includes as much information as possible found in the given article, "
                        f"covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? "
                        f"Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. "
                        f"Use numbers that are available in the given article - do not make up numbers. "
                        f"It is extremely important that you adhere to the facts and numbers given in the article."
                        f"Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance "
                        f"to a boulevard article."
                        f"The article should be split into atleast 3 paragraphs with '\n' symbols. Generate it based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"The result should not have any characters representing bullet points. Do not create any new information and do not "
                        f"use any information that is not present in the given news article. Do not exaggerate! "
                        f"All generated text should be in the {language} language."
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return ArticleBodyResponse.model_validate_json(
            response.choices[0].message.content
        )

    async def regenerate_article_body(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        old_article: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        response = await acompletion(
            model=self.o1_mini_model,
            response_format=ArticleBodyResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate an article: a detailed news story that includes as much information as possible found in the given article, "
                        f"covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? "
                        f"Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. "
                        f"Use numbers that are available in the given article - do not make up numbers. "
                        f"It is extremely important that you adhere to the facts and numbers given in the article."
                        f"Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance "
                        f"to a boulevard article."
                        f"The article should be split into atleast 3 paragraphs with '\n' symbols. Generate it based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic} and the current headline: {current_headline}"
                        f"Here is the old article: {old_article}. Do not repeat it, and it should not be similiar."
                        f"The result should not have any characters representing bullet points. Do not create any new information and do not "
                        f"use any information that is not present in the given news article. Do not exaggerate! "
                        f"All generated text should be in the {language} language."
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return ArticleBodyResponse.model_validate_json(
            response.choices[0].message.content
        )

    async def generate_tags(
        self,
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        current_article: str | None,
        tag_count: int = 4,
        language: Language = Language.SLOVAK,
    ) -> TagsResponse:
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=TagsResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate {tag_count} tags, starting with a '#' without any spaces. Tags should relate to the article so readers "
                        f"can find it easily and should be all capital letters. Generate them based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic}, the current headline: {current_headline} "
                        f"and the article: {current_article}"
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return TagsResponse.model_validate_json(response.choices[0].message.content)

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
        response = await acompletion(
            model=self.gpt_4o_mini_model,
            response_format=TagsResponse,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate {tag_count} tags, starting with a '#' without any spaces. Tags should relate to the article so readers can find it easily "
                        f"and should be all capital letters. Generate them based on this: "
                        f"scraped news article: {scraped_content}, the selected topic: {selected_topic}, the current headline: {current_headline} "
                        f"and the article: {current_article}"
                        f"Here are the old tags: {old_tags}. Do not repeat them, and they should not be similiar."
                        f"The result should not have any characters representing bullet points. All generated text should be in the {language} "
                        f"language. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return TagsResponse.model_validate_json(response.choices[0].message.content)

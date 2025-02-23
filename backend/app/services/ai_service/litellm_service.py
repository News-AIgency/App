import dspy
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


class GenerateTopicsSignature(dspy.Signature):
    """Generate list of topics based on the topics_count InputField and the scraped news article from scraped_content InputField. No numbering, no introductory text, just topics. The result should not have any characters representing bullet points. The topics should be in the language that the language InputField specifies. Each topic should start with capital letter. The news report should be factual as well as neutral. The output is a list of topics in the topics OutputField."""

    topics_count = dspy.InputField(
        desc="Number of topics to generate", type=int, default=5
    )
    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    topics = dspy.OutputField(desc="Generated topics", type=TopicsResponse)


class GenerateTopics(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_topics = dspy.Predict(GenerateTopicsSignature)

    def forward(
        self, topics_count: int, scraped_content: str, language: Language
    ) -> GenerateTopicsSignature:
        generated_topics = self.generate_topics(
            topics_count=topics_count,
            scraped_content=scraped_content,
            language=language,
        )
        return generated_topics


class GenerateArticleSignature(dspy.Signature):
    """Generate 5 sections based on this scraped news article from scraped_content InputField, and the selected topic from selected_topic InputField. The result should not have any characters representing bullet points. Do not create any new information and do not use any information that is not present in the given news article. Do not exaggerate! The generated fields should not have any resemblance to a boulevard article.All generated text should be in the language that the language InputField specifies. Sections will follow these rules:
    1. Headlines: Generate a number of headlines specified by headlines_count InputField that interpret the news in a human-readable way. Headlines should be between 70 and 110 characters, including spaces. All headlines should start with a capital letter.
    2. Engaging text: Generate an engaging text that will hook the reader. Engaging text should not be longer than 240 characters including spaces. Engaging text will not be a part of the actual news article, but still should relate to the headline and compliment it.
    3. Perex: A short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex will be part of the news article
    4. Article: Write a detailed news story that includes as much information as possible found in the given article, covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. Use numbers that are available in the given article - do not make up numbers. It is extremely important that you adhere to the facts and numbers given in the article. Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance to a boulevard article. The article should be split into at least 3 paragraphs with '\n' symbols.
    5. Tags: Generate a number of tags specified by the tag_count InputField, starting with a '#'. Tags should relate to the article so readers can find it easily and should be all capital letters.
    """

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    headlines_count = dspy.InputField(
        desc="Number of headlines to generate", type=int, default=3
    )
    tag_count = dspy.InputField(desc="Number of tags to generate", type=int, default=4)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    article = dspy.OutputField(desc="Generated article", type=ArticleResponse)


class GenerateArticle(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_article = dspy.Predict(GenerateArticleSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        headlines_count: int,
        tag_count: int,
        language: Language,
    ) -> GenerateArticleSignature:
        generated_article = self.generate_article(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            headlines_count=headlines_count,
            tag_count=tag_count,
            language=language,
        )
        return generated_article


class GenerateHeadlinesSignature(dspy.Signature):
    """Generate a number of new headlines specified by the headlines_count InputField that interpret the news in a human-readable way, based on the scraped news article from scraped_content InputField and the selected_topic InputField. Headlines should be between 70 and 110 characters, including spaces. All headlines should start with a capital letter, meaning the first word will start with a capital letter and the rest will be lower case. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField. Fill in only the headlines field, the other fields should remain null."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    headlines_count = dspy.InputField(
        desc="Number of headlines to generate", type=int, default=3
    )
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    headlines = dspy.OutputField(desc="Generated headlines", type=HeadlineResponse)


class GenerateHeadlines(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_headlines = dspy.Predict(GenerateHeadlinesSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        headlines_count: int,
        language: Language,
    ) -> GenerateHeadlinesSignature:
        generated_headlines = self.generate_headlines(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            headlines_count=headlines_count,
            language=language,
        )
        return generated_headlines


class RegenerateHeadlinesSignature(dspy.Signature):
    """Generate a number of new headlines specified by the headlines_count InputField that interpret the news in a human-readable way, based on the scraped news article from scraped_content InputField and the selected_topic InputField. Headlines should be between 70 and 110 characters, including spaces. All headlines should start with a capital letter, meaning the first word will start with a capital letter and the rest will be lower case. The old headlines are in the old_headlines InputField. Do not repeat them, and the new headlines should not be similiar. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField. Fill in only the headlines field, the other fields should remain null."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    old_headlines = dspy.InputField(desc="Old headlines", type=str)
    headlines_count = dspy.InputField(
        desc="Number of headlines to generate", type=int, default=3
    )
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    headlines = dspy.OutputField(desc="Generated headlines", type=HeadlineResponse)


class RegenerateHeadlines(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.regenerate_headlines = dspy.Predict(RegenerateHeadlinesSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        old_headlines: str,
        headlines_count: int,
        language: Language,
    ) -> RegenerateHeadlinesSignature:
        generated_headlines = self.regenerate_headlines(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_headlines=old_headlines,
            headlines_count=headlines_count,
            language=language,
        )
        return generated_headlines


class GenerateEngagingTextSignature(dspy.Signature):
    """Generate an engaging text that will hook the reader, based on the scraped_content InputField and the selected_topic InputField and the current_headline InputField Engaging text should not be longer than 240 characters including spaces. Engaging text will not be a part of the actual news article, but still should relate to the headline and compliment it. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField. Fill in only the engaging text field, the other fields should remain null."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    engaging_text = dspy.OutputField(
        desc="Generated engaging text", type=EngagingTextResponse
    )


class GenerateEngagingText(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_engaging_text = dspy.Predict(GenerateEngagingTextSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        current_headline: str,
        language: Language,
    ) -> GenerateEngagingTextSignature:
        generated_engaging_text = self.generate_engaging_text(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )
        return generated_engaging_text


class RegenerateEngagingTextSignature(dspy.Signature):
    """Generate an engaging text that will hook the reader, based on the scraped_content InputField and the selected_topic InputField and the current_headline InputField. Engaging text should not be longer than 240 characters including spaces. Engaging text will not be a part of the actual news article, but still should relate to the headline and compliment it. The old engaging text is in the old_engaging_text InputField. Do not repeat it, and it should not be similiar. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField. Fill in only the engaging text field, the other fields should remain null."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    old_engaging_text = dspy.InputField(desc="Old engaging text", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    engaging_text = dspy.OutputField(
        desc="Generated engaging text", type=EngagingTextResponse
    )


class RegenerateEngagingText(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.regenerate_engaging_text = dspy.Predict(RegenerateEngagingTextSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        old_engaging_text: str,
        current_headline: str,
        language: Language,
    ) -> RegenerateEngagingTextSignature:
        generated_engaging_text = self.regenerate_engaging_text(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_engaging_text=old_engaging_text,
            current_headline=current_headline,
            language=language,
        )
        return generated_engaging_text


class GeneratePerexSignature(dspy.Signature):
    """Generate a perex: a short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex will be part of the news article. Generate it based on this: scraped news article from scraped_content InputField, the selected topic from selected_topic InputField and the current headline from current_headline InputField. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    perex = dspy.OutputField(desc="Generated perex", type=PerexResponse)


class GeneratePerex(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_perex = dspy.Predict(GeneratePerexSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        current_headline: str,
        language: Language,
    ) -> GeneratePerexSignature:
        generated_perex = self.generate_perex(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )
        return generated_perex


class RegeneratePerexSignature(dspy.Signature):
    """Generate a perex: a short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence should be interesting, but not too long to avoid truncation. Unlike 'Engaging text', perex will be part of the news article. Generate it based on this: scraped news article from the scraped_content InputField, the selected topic from the selected_topic InputField and the current headline from the current_headline InputField. The old perex is in the old_perex InputField. Do not repeat it, and it should not be similiar. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    old_perex = dspy.InputField(desc="Old perex", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    perex = dspy.OutputField(desc="Generated perex", type=PerexResponse)


class RegeneratePerex(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.regenerate_perex = dspy.Predict(RegeneratePerexSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        old_perex: str,
        current_headline: str,
        language: Language,
    ) -> RegeneratePerexSignature:
        generated_perex = self.regenerate_perex(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_perex=old_perex,
            current_headline=current_headline,
            language=language,
        )
        return generated_perex


class GenerateArticleBodySignature(dspy.Signature):
    """Generate an article: a detailed news story that includes as much information as possible found in the given article, covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. Use numbers that are available in the given article - do not make up numbers. It is extremely important that you adhere to the facts and numbers given in the article. Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance to a boulevard article. The article should be split into atleast 3 paragraphs with '\n' symbols. Generate it based on this: scraped news article from the scraped_content InputField, the selected topic from the selected_topic InputField and the current headline from the current_headline InputField. The result should not have any characters representing bullet points. Do not create any new information and do not use any information that is not present in the given news article. Do not exaggerate! All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    article = dspy.OutputField(desc="Generated article", type=ArticleBodyResponse)


class GenerateArticleBody(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_article_body = dspy.Predict(GenerateArticleBodySignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        current_headline: str,
        language: Language,
    ) -> GenerateArticleBodySignature:
        generated_article = self.generate_article_body(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            language=language,
        )
        return generated_article


class RegenerateArticleBodySignature(dspy.Signature):
    """Generate an article: a detailed news story that includes as much information as possible found in the given article, covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. Use numbers that are available in the given article - do not make up numbers. It is extremely important that you adhere to the facts and numbers given in the article. Stick to factual reporting without adding commentary or opinions. The generated article should not have any resemblance to a boulevard article. The article should be split into atleast 3 paragraphs with '\n' symbols. Generate it based on this: scraped news article from the scraped_content InputField, the selected topic from the selected_topic InputField and the current headline from the current_headline InputField. The old article is in the old_article InputField. Do not repeat it, and it should not be similiar. The result should not have any characters representing bullet points. Do not create any new information and do not use any information that is not present in the given news article. Do not exaggerate! All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    old_article = dspy.InputField(desc="Old article", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    article = dspy.OutputField(desc="Generated article", type=ArticleBodyResponse)


class RegenerateArticleBody(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.regenerate_article_body = dspy.Predict(RegenerateArticleBodySignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        old_article: str,
        current_headline: str,
        language: Language,
    ) -> RegenerateArticleBodySignature:
        generated_article = self.regenerate_article_body(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_article=old_article,
            current_headline=current_headline,
            language=language,
        )
        return generated_article


class GenerateTagsSignature(dspy.Signature):
    """Generate a number of tags specified by the tag_count InputField, starting with a '#' without any spaces. Tags should relate to the article so readers can find it easily and should be all capital letters. Generate them based on this: scraped news article from the scraped_content InputField, the selected topic from the selected_topic InputField, the current headline from the current_headline InputField and the article from the current_article InputField. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    current_headline = dspy.InputField(desc="Current headline", type=str)
    current_article = dspy.InputField(desc="Current article", type=str)
    tag_count = dspy.InputField(desc="Number of tags to generate", type=int, default=4)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    tags = dspy.OutputField(desc="Generated tags", type=TagsResponse)


class GenerateTags(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.generate_tags = dspy.Predict(GenerateTagsSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        current_headline: str,
        current_article: str,
        tag_count: int,
        language: Language,
    ) -> GenerateTagsSignature:
        generated_tags = self.generate_tags(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            current_headline=current_headline,
            current_article=current_article,
            tag_count=tag_count,
            language=language,
        )
        return generated_tags


class RegenerateTagsSignature(dspy.Signature):
    """Generate a number of tags specified by the tag_count InputField, starting with a '#' without any spaces. Tags should relate to the article so readers can find it easily and should be all capital letters. Generate them based on this: scraped news article from the  scraped_content InputField, the selected topic from the selected_topic InputField, the current headline from the current_headline InputField and the article from the current_article InputField. The old tags are in the old_tags InputField. Do not repeat them, and they should not be similiar. The result should not have any characters representing bullet points. All generated text should be in the language specified by the language InputField."""

    scraped_content = dspy.InputField(desc="Scraped news article", type=str)
    selected_topic = dspy.InputField(desc="Selected news article topic", type=str)
    old_tags = dspy.InputField(desc="Old tags", type=list[str])
    current_headline = dspy.InputField(desc="Current headline", type=str)
    current_article = dspy.InputField(desc="Current article", type=str)
    tag_count = dspy.InputField(desc="Number of tags to generate", type=int, default=4)
    language = dspy.InputField(
        desc="Language of the news article", type=Language, default=Language.SLOVAK
    )
    tags = dspy.OutputField(desc="Generated tags", type=TagsResponse)


class RegenerateTags(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.regenerate_tags = dspy.Predict(RegenerateTagsSignature)

    def forward(
        self,
        scraped_content: str,
        selected_topic: str,
        old_tags: list[str],
        current_headline: str,
        current_article: str,
        tag_count: int,
        language: Language,
    ) -> RegenerateTagsSignature:
        generated_tags = self.regenerate_tags(
            scraped_content=scraped_content,
            selected_topic=selected_topic,
            old_tags=old_tags,
            current_headline=current_headline,
            current_article=current_article,
            tag_count=tag_count,
            language=language,
        )
        return generated_tags


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

        return TopicsResponse.model_validate_json(generated_topics.topics)

    async def generate_article(
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

        return ArticleResponse.model_validate_json(generated_article.article)

    async def generate_headlines(
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

        return HeadlineResponse.model_validate_json(generated_headlines.headlines)

    async def regenerate_headlines(
        scraped_content: str | None,
        selected_topic: str | None,
        old_headlines: str | None,
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

        return HeadlineResponse.model_validate_json(generated_headlines.headlines)

    async def generate_engaging_text(
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

        return EngagingTextResponse.model_validate_json(
            generated_engaging_text.engaging_text
        )

    async def regenerate_engaging_text(
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

        return EngagingTextResponse.model_validate_json(
            generated_engaging_text.engaging_text
        )

    async def generate_perex(
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

        return PerexResponse.model_validate_json(generated_perex.perex)

    async def regenerate_perex(
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

        return PerexResponse.model_validate_json(generated_perex.perex)

    async def generate_article_body(
        scraped_content: str | None,
        selected_topic: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        lm = dspy.LM(
            "openai/o1_mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
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

        return ArticleBodyResponse.model_validate_json(generated_article.article)

    async def regenerate_article_body(
        scraped_content: str | None,
        selected_topic: str | None,
        old_article: str | None,
        current_headline: str | None,
        language: Language = Language.SLOVAK,
    ) -> ArticleBodyResponse:
        lm = dspy.LM(
            "openai/o1_mini",
            api_key=settings.LITE_LLM_KEY,
            base_url="http://147.175.151.44/",
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

        return ArticleBodyResponse.model_validate_json(generated_article.article)

    async def generate_tags(
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

        return TagsResponse.model_validate_json(generated_tags.tags)

    async def regenerate_tags(
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

        return TagsResponse.model_validate_json(generated_tags.tags)

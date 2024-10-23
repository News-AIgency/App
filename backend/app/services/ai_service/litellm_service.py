from App.backend.app.core.config import settings
from litellm import completion


class LiteLLMService:

    def __init__(self) -> None:
        self.api_key = settings.LITE_LLM_KEY
        self.litellm_url = "http://147.175.151.44/"
        self.model = "gpt-4o-mini"

    def test_litellm(self) -> str:
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "this is a test request, write a short poem",
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        return response["choices"][0]["message"]["content"]

    def generate_topics(self, scraped_content: str | None) -> list[str]:
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate list of 5 topics based on this scraped news article: {scraped_content}. "
                    f"No numbering, no introductory text, just topics. The result should not have any "
                    f"characters representing bullet points. The topics should be in the same language "
                    f"as the news article.",
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        topics_text = response.choices[0].message.content.strip()
        topics = [topic.strip() for topic in topics_text.split("\n") if topic.strip()]

        return topics

    def generate_article(self, scraped_content: str | None) -> list[list[str]]:
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate three sections based on this scraped news article: {scraped_content}. "
                        f"Sections should be separated by a semicolon (';') and should follow the rules below: "
                        f"1. Headlines: Generate at least 3 headlines that interpret the news in a human-readable way. Headlines should "
                        f"not be too long to avoid truncation. Use '\n' to separate individual headlines within this section. "
                        f"2. Perex: A short, engaging text of 140-160 characters that complements the headlines and attracts readers. The first sentence "
                        f"should be interesting, but not too long to avoid truncation. "
                        f"3. Main Article: Write a detailed news story that includes as much information as possible found in the scraped content, "
                        f"covering the following key questions: Who? What? Where? When? Why (most important)? How (most important)? How much? "
                        f"Include quotes if they are available, specifying who said it, what was said, where and when it was said, and for whom. "
                        f"Stick to factual reporting without adding commentary or opinions. "
                        f"Ensure that the entire output is formatted with sections separated by ';' and each headline divided by '\n'. "
                    ),
                }
            ],
            api_key=self.api_key,
            base_url=self.litellm_url,
        )

        response_text = response.choices[0].message.content.strip()
        sections = [
            section.strip() for section in response_text.split(";") if section.strip()
        ]
        split_sections = [section.split("\n") for section in sections]

        return split_sections

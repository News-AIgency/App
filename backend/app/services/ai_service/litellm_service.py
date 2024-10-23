from backend.app.core.config import settings
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

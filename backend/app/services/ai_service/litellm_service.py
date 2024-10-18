from core.config import settings
from litellm import completion


def use_litellm() -> str:
    api_key = settings.LITE_LLM_KEY
    litellm_url = "http://147.175.151.44/"
    model = "gpt-4o-mini"

    response = completion(
        model=model,
        messages=[
            {"role": "user", "content": "this is a test request, write a short poem"}
        ],
        api_key=api_key,
        base_url=litellm_url,
    )

    return response["choices"][0]["message"]["content"]

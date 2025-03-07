import dspy

from backend.app.core.config import settings

lm = dspy.LM(
    "openai/gpt-4o-mini",
    api_key=settings.LITE_LLM_KEY,
    base_url="http://147.175.151.44/",
)
dspy.settings.configure(lm=lm, async_max_workers=8)


class LlmJudgeSignature(dspy.Signature):
    """Compare the two strings str_1 and str_2. Output an integer, similarity, that represents how close or similar the two strings are. The similarity output must be an integer between 0 and 100. The higher the number the more similar the two strings are. If the are nothing alike, it should be 0, if the are totally the same, it should be 100."""

    str_1 = dspy.InputField(type=str, desc="The first string to compare")
    str_2 = dspy.InputField(type=str, desc="The second string to compare")
    similarity: int = dspy.OutputField(
        type=int, desc="The similarity of the two input strings from 0 to 100"
    )


class LlmJudge(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.compare_strings = dspy.Predict(LlmJudgeSignature)

    def forward(self, str_1: str, str_2: str) -> LlmJudgeSignature:
        response = self.compare_strings(str_1=str_1, str_2=str_2)
        return response.similarity / 100


async def llm_compare_strings(string_1: str, string_2: str) -> float:
    compare_string_program = LlmJudge()
    compare_string_program = dspy.asyncify(compare_string_program)
    similarity = await compare_string_program(string_1, string_2)
    return similarity

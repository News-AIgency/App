from typing import Any

import language_tool_python
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.utils.default_article import default_article
from backend.app.utils.language_enum import LanguageToolLanguage

router = APIRouter()


class GrammarRequest(BaseModel):
    text: str
    language: LanguageToolLanguage = LanguageToolLanguage.SLOVAK


@router.post("/check-grammar")
async def check_grammar(request: GrammarRequest) -> dict[str, Any]:
    tool = language_tool_python.LanguageTool(request.language.value)

    matches = tool.check(request.text)

    issues = []
    for match in matches:
        issues.append(
            {
                "message": match.message,
                "offset": match.offset,
                "length": match.errorLength,
                "replacements": match.replacements,
                "rule_id": match.ruleId,
                "context": {"text": match.context, "offset": match.offsetInContext},
            }
        )

    return {"issues": issues}


def correct_text(
    text: str, language: LanguageToolLanguage = LanguageToolLanguage.SLOVAK
) -> str:
    # disable MORFOLOGIK_RULE_SK to avoid over-correction of unknown words
    tool = language_tool_python.LanguageTool(
        language.value, config={"disabledRuleIds": ["MORFOLOGIK_RULE_SK"]}
    )
    matches = tool.check(text)

    # Reverse order so that it starts fixing from the back to make sure offsets for the other replacements still fit
    matches.sort(key=lambda m: m.offset, reverse=True)

    for match in matches:
        word = text[match.offset : match.offset + match.errorLength]

        # If word contains a capital letter, don't fix it, likely a proper noun
        if not word.islower():
            continue

        if match.replacements:
            replacement = match.replacements[0]
            text = (
                text[: match.offset]
                + replacement
                + text[match.offset + match.errorLength :]
            )

    return text


if __name__ == "__main__":
    # print(default_article)
    print(correct_text(default_article))

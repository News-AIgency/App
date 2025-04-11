from enum import Enum


class Language(Enum):
    SLOVAK = "slovak"
    ENGLISH = "english"


class LanguageToolLanguage(Enum):
    SLOVAK = "sk"
    ENGLISH = "en-US"


# Mapping between enums
LANGUAGE_TO_TOOL_LANG = {
    Language.SLOVAK: LanguageToolLanguage.SLOVAK,
    Language.ENGLISH: LanguageToolLanguage.ENGLISH,
}

from typing import Any, Literal

import dspy
from dspy import InputField, OutputField, Signature

from backend.app.services.ai_service.dspy_signature_guidelines import (
    GENERATE_ARTICLE_DOC,
    GENERATE_ENGAGING_TEXT_DOC,
    GENERATE_HEADLINES_DOC,
    GENERATE_PEREX_DOC,
    GENERATE_TAGS_DOC,
    GRAPHS_GUIDELINES_DOC,
    REGENERATE_ARTICLE_DOC,
    REGENERATE_ENGAGING_TEXT_DOC,
    REGENERATE_HEADLINES_DOC,
    REGENERATE_PEREX_DOC,
    REGENERATE_TAGS_DOC,
    STORM_GENERATE_ARTICLE_DOC,
    STORM_GENERATE_ENGAGING_TEXT_DOC,
    STORM_GENERATE_PEREX_DOC,
    STORM_REGENERATE_ARTICLE_DOC,
    STORM_REGENERATE_ENGAGING_TEXT_DOC,
    STORM_REGENERATE_PEREX_DOC,
    TOPICS_GUIDELINES_DOC,
)
from backend.app.services.ai_service.response_models import (
    ArticleBodyResponse,
    EngagingTextResponse,
    HeadlineResponse,
    PerexResponse,
    TagsResponse,
    TopicsResponse,
)
from backend.app.utils.language_enum import Language


class BasePredictModule(dspy.Module):
    def __init__(self, signature_cls: type) -> None:
        super().__init__()
        self._predictor = dspy.Predict(signature_cls)

    def forward(self, **kwargs) -> Any:  # noqa: ANN401
        return self._predictor(**kwargs)


def create_signature_class(name: str, config: dict) -> type:
    """Programmatically construct the class using a configuration dictionary that specifies input and output fields,
    including their types, descriptions, and optional default values"""

    attrs: dict = {"__doc__": config.get("doc", "")}
    annotations: dict = {}
    # Input fields
    for field_name, field_conf in config.get("inputs", {}).items():
        field_type = field_conf["type"]
        # Set default if provided, otherwise no default
        if "default" in field_conf:
            attrs[field_name] = InputField(
                default=field_conf["default"], desc=field_conf.get("desc")
            )
        else:
            attrs[field_name] = InputField(desc=field_conf.get("desc"))
        annotations[field_name] = field_type
    # Output fields
    for field_name, field_conf in config.get("outputs", {}).items():
        field_type = field_conf["type"]
        if "default" in field_conf:
            attrs[field_name] = OutputField(
                default=field_conf["default"], desc=field_conf.get("desc")
            )
        else:
            attrs[field_name] = OutputField(desc=field_conf.get("desc"))
        annotations[field_name] = field_type
    # Attach the __annotations__ to include type hints
    attrs["__annotations__"] = annotations

    return type(name, (Signature,), attrs)


SIGNATURE_CONFIG = {
    "GenerateTopicsSignature": {
        "doc": TOPICS_GUIDELINES_DOC,
        "inputs": {
            "topics_count": {
                "type": int,
                "default": 5,
                "desc": "Number of topics to generate.",
            },
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {"topics": {"type": TopicsResponse, "desc": "Generated topics."}},
    },
    "GenerateHeadlinesSignature": {
        "doc": GENERATE_HEADLINES_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected news article topic."},
            "headlines_count": {
                "type": int,
                "default": 3,
                "desc": "Number of headlines to generate.",
            },
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {
            "headlines": {"type": HeadlineResponse, "desc": "Generated headlines."}
        },
    },
    "RegenerateHeadlinesSignature": {
        "doc": REGENERATE_HEADLINES_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected news article topic."},
            "old_headlines": {"type": str, "desc": "Old headlines."},
            "headlines_count": {
                "type": int,
                "default": 3,
                "desc": "Number of headlines to generate.",
            },
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {
            "headlines": {"type": HeadlineResponse, "desc": "Generated headlines."}
        },
    },
    "GenerateEngagingTextSignature": {
        "doc": GENERATE_ENGAGING_TEXT_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected topic."},
            "current_headline": {"type": str, "desc": "Current headline."},
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {
            "engaging_text": {
                "type": EngagingTextResponse,
                "desc": "Generated engaging text.",
            }
        },
    },
    "StormGenerateEngagingTextSignature": {
        "doc": STORM_GENERATE_ENGAGING_TEXT_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article"},
            "storm_article": {"type": str, "desc": "Storm-generated article"},
            "selected_topic": {"type": str, "desc": "Selected topic"},
            "current_headline": {"type": str, "desc": "Headline for context"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "engaging_text": {
                "type": EngagingTextResponse,
                "desc": "Generated engaging text",
            }
        },
    },
    "RegenerateEngagingTextSignature": {
        "doc": REGENERATE_ENGAGING_TEXT_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article"},
            "selected_topic": {"type": str, "desc": "Selected topic"},
            "old_engaging_text": {"type": str, "desc": "Previous engaging text"},
            "current_headline": {"type": str, "desc": "Headline for context"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "engaging_text": {
                "type": EngagingTextResponse,
                "desc": "Regenerated engaging text",
            }
        },
    },
    "StormRegenerateEngagingTextSignature": {
        "doc": STORM_REGENERATE_ENGAGING_TEXT_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article"},
            "storm_article": {"type": str, "desc": "Storm-generated article"},
            "selected_topic": {"type": str, "desc": "Selected topic"},
            "old_engaging_text": {"type": str, "desc": "Old engaging text"},
            "current_headline": {"type": str, "desc": "Headline for context"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "engaging_text": {
                "type": EngagingTextResponse,
                "desc": "Regenerated engaging text",
            }
        },
    },
    "GeneratePerexSignature": {
        "doc": GENERATE_PEREX_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected news article topic."},
            "current_headline": {"type": str, "desc": "Current headline."},
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {"perex": {"type": PerexResponse, "desc": "Generated perex."}},
    },
    "StormGeneratePerexSignature": {
        "doc": STORM_GENERATE_PEREX_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article"},
            "storm_article": {"type": str, "desc": "Storm-generated article content"},
            "selected_topic": {"type": str, "desc": "Selected topic of the article"},
            "current_headline": {
                "type": str,
                "desc": "Current headline to align the perex with",
            },
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {"perex": {"type": PerexResponse, "desc": "Generated perex text"}},
    },
    "RegeneratePerexSignature": {
        "doc": REGENERATE_PEREX_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article"},
            "selected_topic": {"type": str, "desc": "Topic of the news article"},
            "old_perex": {"type": str, "desc": "Previous perex text"},
            "current_headline": {"type": str, "desc": "Headline the perex refers to"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {"perex": {"type": PerexResponse, "desc": "Regenerated perex text"}},
    },
    "StormRegeneratePerexSignature": {
        "doc": STORM_REGENERATE_PEREX_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article"},
            "storm_article": {"type": str, "desc": "Storm article"},
            "selected_topic": {"type": str, "desc": "Selected topic"},
            "old_perex": {"type": str, "desc": "Old perex"},
            "current_headline": {"type": str, "desc": "Headline context"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {"perex": {"type": PerexResponse, "desc": "Regenerated perex"}},
    },
    "GenerateArticleBodySignature": {
        "doc": GENERATE_ARTICLE_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected news article topic."},
            "current_headline": {"type": str, "desc": "Current headline."},
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {
            "article": {"type": ArticleBodyResponse, "desc": "Generated article body."}
        },
    },
    "StormGenerateArticleBodySignature": {
        "doc": STORM_GENERATE_ARTICLE_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article"},
            "storm_article": {
                "type": str,
                "desc": "Storm-generated article to enrich output",
            },
            "selected_topic": {"type": str, "desc": "Selected topic of the article"},
            "current_headline": {"type": str, "desc": "Current headline for context"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "article": {"type": ArticleBodyResponse, "desc": "Generated article body"}
        },
    },
    "RegenerateArticleBodySignature": {
        "doc": REGENERATE_ARTICLE_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article source"},
            "selected_topic": {"type": str, "desc": "Topic of the article"},
            "old_article": {"type": str, "desc": "Old article body to avoid repeating"},
            "current_headline": {"type": str, "desc": "Current headline"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "article": {"type": ArticleBodyResponse, "desc": "Regenerated article body"}
        },
    },
    "StormRegenerateArticleBodySignature": {
        "doc": STORM_REGENERATE_ARTICLE_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped article"},
            "storm_article": {"type": str, "desc": "Storm article"},
            "selected_topic": {"type": str, "desc": "Topic"},
            "old_article": {"type": str, "desc": "Old article"},
            "current_headline": {"type": str, "desc": "Headline"},
            "language": {
                "type": Language,
                "desc": Language.SLOVAK,
                "default": "Language.SLOVAK",
            },
        },
        "outputs": {
            "article": {"type": ArticleBodyResponse, "desc": "Regenerated article body"}
        },
    },
    "GenerateTagsSignature": {
        "doc": GENERATE_TAGS_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article."},
            "selected_topic": {"type": str, "desc": "Selected news article topic."},
            "current_headline": {"type": str, "desc": "Current headline."},
            "current_article": {"type": str, "desc": "Current article body."},
            "tag_count": {
                "type": int,
                "default": 4,
                "desc": "Number of tags to generate.",
            },
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {"tags": {"type": TagsResponse, "desc": "Generated tags."}},
    },
    "RegenerateTagsSignature": {
        "doc": REGENERATE_TAGS_DOC,
        "inputs": {
            "article_text": {
                "type": str,
                "desc": "The article content to extract tags from.",
            },
            "count": {"type": int, "default": 5, "desc": "Number of tags to generate."},
        },
        "outputs": {
            "tags": {"type": list[str], "desc": "List of regenerated tags or keywords."}
        },
    },
    "GenerateGraphsSignature": {
        "doc": GRAPHS_GUIDELINES_DOC,
        "inputs": {
            "scraped_content": {"type": str, "desc": "Scraped news article content."},
            "language": {
                "type": Language,
                "default": Language.SLOVAK,
                "desc": "Language of the news article.",
            },
        },
        "outputs": {
            "gen_graph": {"type": bool, "desc": "Whether a graph should be generated."},
            "graph_type": {
                "type": Literal["pie", "line", "bar", "histogram", "scatter"],
                "desc": "Type of graph best suited for the article.",
            },
            "graph_data": {
                "type": dict,
                "desc": (
                    "Graph data structure. Depends on graph_type:\n"
                    "- Pie, bar, line, histogram: {{labels: [...], values: [...]}}\n"
                    "- Histogram: labels can be None\n"
                    "- Scatter: {{x_vals: [...], y_vals: [...]}}"
                ),
            },
        },
    },
}

SIGNATURE_CLASSES = {
    name: create_signature_class(name, conf) for name, conf in SIGNATURE_CONFIG.items()
}


class GenerateTopics(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateTopicsSignature"])


class GenerateHeadlines(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateHeadlinesSignature"])


class RegenerateHeadlines(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["RegenerateHeadlinesSignature"])


class GenerateEngagingText(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateEngagingTextSignature"])


class StormGenerateEngagingText(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormGenerateEngagingTextSignature"])


class RegenerateEngagingText(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["RegenerateEngagingTextSignature"])


class StormRegenerateEngagingText(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormRegenerateEngagingTextSignature"])


class GeneratePerex(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GeneratePerexSignature"])


class StormGeneratePerex(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormGeneratePerexSignature"])


class RegeneratePerex(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["RegeneratePerexSignature"])


class StormRegeneratePerex(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormRegeneratePerexSignature"])


class GenerateArticleBody(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateArticleBodySignature"])


class StormGenerateArticleBody(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormGenerateArticleBodySignature"])


class RegenerateArticleBody(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["RegenerateArticleBodySignature"])


class StormRegenerateArticleBody(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["StormRegenerateArticleBodySignature"])


class GenerateTags(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateTagsSignature"])


class RegenerateTags(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["RegenerateTagsSignature"])


class GenerateGraphs(BasePredictModule):
    def __init__(self) -> None:
        super().__init__(SIGNATURE_CLASSES["GenerateGraphsSignature"])

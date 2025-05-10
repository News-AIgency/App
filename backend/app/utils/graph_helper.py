import ast
from typing import Any

from backend.app.services.ai_service.response_models import ArticleResponse


def clean_graph_data(article: ArticleResponse) -> ArticleResponse:
    if not (article.gen_graph and article.graph_data):
        return

    graph_labels_key = "x_vals" if article.graph_type == "scatter" else "labels"
    graph_values_key = "y_vals" if article.graph_type == "scatter" else "values"

    labels = article.graph_data.get(graph_labels_key, [])
    values = article.graph_data.get(graph_values_key, [])

    # Attempt to parse labels and values if they are strings and not individual elements in a list
    if isinstance(labels, list) and all(isinstance(item, str) for item in labels):
        try:
            labels = ast.literal_eval(f"[{labels[0]}]") if len(labels) == 1 else labels
        except (ValueError, SyntaxError):
            labels = []

    if isinstance(values, list) and all(isinstance(item, str) for item in values):
        try:
            values = ast.literal_eval(f"[{values[0]}]") if len(values) == 1 else values
        except (ValueError, SyntaxError):
            values = []

    # Need to also filter labels and values, sometimes it has none values and therefore it is necessary to also
    # remove corresponding element from the other dict to prevent mismatch, except for histogram, which has labels = None
    if article.graph_type != "histogram":
        filtered_labels = []
        filtered_values = []
        for label, value in zip(labels, values):
            if value is not None:
                filtered_labels.append(label)
                filtered_values.append(value)

        # Check if after filtering it, still has enough datapoints to create a graph
        if len(filtered_labels) >= 2:
            article.graph_data[graph_labels_key] = filtered_labels
            article.graph_data[graph_values_key] = filtered_values
        else:
            # If not enough valid points, disable graph
            article.gen_graph = False
            article.graph_data = None

    return article


def generate_article_data(
    url: str, article: ArticleResponse, selected_topic: str
) -> dict[str, Any]:
    article_data = {
        "url": {"url": url},
        "heading": {"heading_content": article.headlines[0]},
        "topic": {"topic_content": selected_topic},
        "perex": {"perex_content": article.perex},
        "body": {"body_content": article.article},
        "engaging_text": {"engaging_text_content": article.engaging_text},
        "tags": [{"tags_content": tag} for tag in article.tags],
    }

    if article.gen_graph:
        graph_labels_key = "x_vals" if article.graph_type == "scatter" else "labels"
        graph_values_key = "y_vals" if article.graph_type == "scatter" else "values"

        article_data["graph_data"] = {
            "graph_title": article.graph_title,
            "graph_type": article.graph_type,
            "graph_axis_labels": article.graph_axis_labels,
            "graph_labels": article.graph_data[graph_labels_key],
            "graph_values": article.graph_data[graph_values_key],
        }
    return article_data

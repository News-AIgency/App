from typing import Any

from backend.app.services.ai_service.response_models import ArticleResponse


def clean_graph_data(article: ArticleResponse) -> ArticleResponse:
    if not (article.gen_graph and article.graph_data):
        return

    graph_labels_key = "x_vals" if article.graph_type == "scatter" else "labels"
    graph_values_key = "y_vals" if article.graph_type == "scatter" else "values"

    labels = article.graph_data.get(graph_labels_key, [])
    values = article.graph_data.get(graph_values_key, [])

    # Need to also filter labels and values, sometimes it has none values and therefore it is necessary to also
    # remove corresponding element from the other dict to prevent mismatch
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
            "graph_type": article.graph_type,
            "graph_labels": article.graph_data[graph_labels_key],
            "graph_values": article.graph_data[graph_values_key],
        }
    return article_data

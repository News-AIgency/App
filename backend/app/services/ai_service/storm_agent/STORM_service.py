import json
import os
from os import PathLike
from typing import Any

import knowledge_storm
from knowledge_storm import (
    OpenAIModel,
    QdrantVectorStoreManager,
    STORMWikiLMConfigs,
    STORMWikiRunner,
    STORMWikiRunnerArguments,
    VectorRM,
)

from backend.app.core.config import settings
from backend.app.utils.default_article import default_article_url, default_topic

OUTPUT_DIR = ".\\services\\ai_service\\storm_agent\\results"
MAX_CONV_TURN = 3
MAX_PERSPECTIVE = 3
SEARCH_TOP_K = 3
MAX_THREAD_NUM = 3
COLLECTION_NAME = "corpus"
EMBEDDING_MODEL = "BAAI/bge-m3"
DEVICE = "cpu"
VECTOR_STORE_DIR = ".\\services\\ai_service\\storm_agent\\vector_store"

CSV_FILE_PATH = ".\\output_file.csv"
EMBED_BATCH_SIZE = 64


# region Embedding pipeline
def embedding_pipeline() -> None:
    # Create / update the vector store with the documents in the csv file
    kwargs = {
        "file_path": CSV_FILE_PATH,
        "content_column": "content",
        "title_column": "title",
        "url_column": "url",
        "desc_column": "description",
        "batch_size": EMBED_BATCH_SIZE,
        "vector_db_mode": "offline",
        "collection_name": COLLECTION_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "device": "cuda",
    }
    QdrantVectorStoreManager.create_or_update_vector_store(
        vector_store_path=VECTOR_STORE_DIR, **kwargs
    )


# endregion


# region STORM Agents
def set_agents_personas() -> None:
    pass


# endregion


# region Fix article generation
def generate_references_footer(selected_topic: str) -> tuple[list[dict[str, Any]], str]:
    """
    STORM tends to skip references section in footer, therefore we force generate it from
    the url_to_info.json file instead.
    :return:
        str: Generated references footer section
    """
    url_to_info_path = os.path.join(
        os.path.join(OUTPUT_DIR, selected_topic), "url_to_info.json"
    )
    with open(url_to_info_path) as f:
        data = json.load(f)

    # Parsing the json with references necessary for constructing markdown reference link
    parsed_data = [
        {
            "key": data["url_to_unified_index"][url],
            "title": data["url_to_info"][url]["title"],
            "url": url,
        }
        for url in data["url_to_unified_index"]
    ]

    # Sort the parsed_data list by the 'key' field
    parsed_data.sort(key=lambda x: x["key"])

    # Formating each entry in parsed json to the markdown reference link format
    markdown_references = [
        f"- {reference['key']}  [{reference['title']}]({reference['url']})"
        for reference in parsed_data
    ]

    return parsed_data, "\n".join(markdown_references)


def create_finalized_article(selected_topic: str) -> str:
    """
    Getting the polished article from filesystem, generating and appending the references footer and saves it in cache.
    :param result_directory:
    """

    parsed_references, references_footer = generate_references_footer(selected_topic)

    with open(
        os.path.join(
            os.path.join(OUTPUT_DIR, selected_topic), "storm_gen_article_polished.txt"
        ),
        encoding="utf-8",
    ) as f:
        text = f.read()

    for ref in parsed_references:
        text = text.replace(f"[{ref['key']}]", rf"\[[{ref['key']}]({ref['url']})\]")

    text += f"\n\n## References\n\n{references_footer}"

    print(text)
    return text


# endregion

# region Run STORM


# STORM file writing util method does not have utf-8 encoding
# Therefore monkey-patch is needed to prevent from crashing when in writing slovak language
def file_write_utf8(
    s: str, path: int | str | bytes | PathLike[str] | PathLike[bytes]
) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def monkey_patch_storm() -> None:
    knowledge_storm.utils.FileIOHelper.write_str = file_write_utf8


def run_storm(selected_topic: str, article_url: str) -> str:
    # Get the absolute path of the current script
    current_file_path = os.path.abspath(__file__)

    # Get the directory of the current script
    current_directory = os.path.dirname(current_file_path)

    print("Current file location:", current_file_path)
    print("Current directory:", current_directory)

    # Setting custom methods for STORM
    monkey_patch_storm()

    print("Loading corpus...")

    engine_lm_configs = STORMWikiLMConfigs()

    openai_kwargs = {
        "api_key": settings.LITE_LLM_KEY,
        "api_base": "http://147.175.151.44/",
        "temperature": 1.0,
        "top_p": 0.9,
    }

    model_class = OpenAIModel
    gpt_o4_mini_name = "gpt-4o-mini"

    # Try to use more powerful models to generate reliable text and citations, at least for article_gen_lm
    conv_simulator_lm = model_class(
        model=gpt_o4_mini_name, max_tokens=500, **openai_kwargs
    )
    question_asker_lm = model_class(
        model=gpt_o4_mini_name, max_tokens=500, **openai_kwargs
    )
    outline_gen_lm = model_class(
        model=gpt_o4_mini_name, max_tokens=400, **openai_kwargs
    )
    article_gen_lm = model_class(
        model=gpt_o4_mini_name, max_tokens=700, **openai_kwargs
    )
    article_polish_lm = model_class(
        model=gpt_o4_mini_name, max_tokens=4000, **openai_kwargs
    )

    engine_lm_configs.set_conv_simulator_lm(conv_simulator_lm)
    engine_lm_configs.set_question_asker_lm(question_asker_lm)
    engine_lm_configs.set_outline_gen_lm(outline_gen_lm)
    engine_lm_configs.set_article_gen_lm(article_gen_lm)
    engine_lm_configs.set_article_polish_lm(article_polish_lm)

    # Initialize the engine arguments
    engine_args = STORMWikiRunnerArguments(
        output_dir=OUTPUT_DIR,
        max_conv_turn=MAX_CONV_TURN,
        max_perspective=MAX_PERSPECTIVE,
        search_top_k=SEARCH_TOP_K,
        max_thread_num=MAX_THREAD_NUM,
    )

    # Setup VectorRM to retrieve information from own corpus
    rm = VectorRM(
        collection_name=COLLECTION_NAME,
        embedding_model=EMBEDDING_MODEL,
        device=DEVICE,
        k=SEARCH_TOP_K,
    )

    # Initialize the vector store offline (stored the db locally):
    rm.init_offline_vector_db(vector_store_path=VECTOR_STORE_DIR)

    # Initialize the STORM Wiki Runner
    runner = STORMWikiRunner(engine_args, engine_lm_configs, rm)

    # TODO: Set instruction for agent here

    print("Running STORM agent...")
    # Running the pipeline
    topic = selected_topic
    runner.run(
        topic=topic,
        ground_truth_url=article_url,
        do_research=True,
        do_generate_outline=True,
        do_generate_article=True,
        do_polish_article=True,
    )
    runner.post_run()
    runner.summary()

    return create_finalized_article(selected_topic.replace(" ", "_"))


# endregion

if __name__ == "__main__":
    selected_topic = default_topic
    article_url = default_article_url
    run_storm(selected_topic, article_url)
    # create_finalized_article(selected_topic.replace(" ", "_"))

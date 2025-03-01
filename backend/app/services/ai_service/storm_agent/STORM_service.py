import json
import os
import tempfile
from typing import Any

import knowledge_storm
from fs.memoryfs import MemoryFS
from knowledge_storm import (
    OpenAIModel,
    STORMWikiLMConfigs,
    STORMWikiRunner,
    STORMWikiRunnerArguments,
    VectorRM,
)
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

import backend.app.services.ai_service.storm_agent.VectorStoreManager
from backend.app.core.config import settings
from backend.app.services.ai_service.storm_agent.FileIOHelper import FileIOHelper
from backend.app.utils.default_article import default_article_url, default_topic

"""
 We need to create temporary in-memory file system for STORM outputs.
 Since STORM only accepts string file-path we need make it so the
 string file-path points towards the in-memory filepath
"""
memory_fs = MemoryFS()

# Create a temporary directory on the real filesystem to "mount" MemoryFS
temp_dir = tempfile.TemporaryDirectory()
OUTPUT_DIR = temp_dir.name  # This makes STORM think it's a normal path

file_io_helper = FileIOHelper(memory_fs)

MAX_CONV_TURN = 3
MAX_PERSPECTIVE = 3
SEARCH_TOP_K = 3
MAX_THREAD_NUM = 3
COLLECTION_NAME = "corpus"
EMBEDDING_MODEL = "BAAI/bge-m3"
DEVICE = "cpu"  # Change to "cuda" if possible
VECTOR_STORE_DIR = ".\\vector_store"

CSV_FILE_PATH = ".\\storm_data.csv"
EMBED_BATCH_SIZE = 64


# region Embedding pipeline
def embedding_pipeline(location: str, port: int) -> None:
    # Create / update the vector store with the documents in the csv file
    kwargs = {
        "file_path": CSV_FILE_PATH,
        "content_column": "content",
        "title_column": "title",
        "url_column": "url",
        "desc_column": "description",
        "batch_size": EMBED_BATCH_SIZE,
        "collection_name": COLLECTION_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "device": DEVICE,
    }

    backend.app.services.ai_service.storm_agent.VectorStoreManager.QdrantVectorStoreManager.create_or_update_vector_store(
        location=location, port=port, **kwargs
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
    print("MemoryFS contents:", memory_fs.listdir("/"))

    url_to_info_path = os.path.join(
        os.path.join(OUTPUT_DIR, selected_topic), "url_to_info.json"
    )

    # Read from MemoryFS instead of disk
    data = json.loads(file_io_helper.read_utf8(url_to_info_path))

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

    article_path = os.path.join(
        OUTPUT_DIR, selected_topic, "storm_gen_article_polished.txt"
    )

    # Read from MemoryFS instead of disk
    text = file_io_helper.read_utf8(article_path)

    for ref in parsed_references:
        text = text.replace(f"[{ref['key']}]", rf"\[[{ref['key']}]({ref['url']})\]")

    text += f"\n\n## References\n\n{references_footer}"

    print(text)

    memory_fs.close()  # Delete the temporary filesystem
    return text


# endregion


# region Run STORM
def monkey_patch_storm() -> None:
    knowledge_storm.utils.FileIOHelper.write_str = file_io_helper.write_utf8
    knowledge_storm.utils.FileIOHelper.load_str = file_io_helper.read_utf8
    knowledge_storm.utils.FileIOHelper.dump_json = file_io_helper.dump_json_memory
    knowledge_storm.utils.FileIOHelper.load_json = file_io_helper.load_json_memory


def init_qdrant_server(rm: VectorRM) -> None:
    try:
        rm.client = QdrantClient("localhost", port=6333)

        """
        Check if the Qdrant collection exists and create it if it does not.
        """
        if rm.client is None:
            raise ValueError("Qdrant client is not initialized.")
        if rm.client.collection_exists(collection_name=f"{rm.collection_name}"):
            print(f"Collection {rm.collection_name} exists. Loading the collection...")
            rm.qdrant = Qdrant(
                client=rm.client,
                collection_name=rm.collection_name,
                embeddings=rm.model,
            )
        else:
            raise ValueError(
                f"Collection {rm.collection_name} does not exist. Please create the collection first."
            )
    except Exception as e:
        raise ValueError(f"Error occurs when connecting to the server: {e}")


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

    # Initialize the vector store on qdrant server
    init_qdrant_server(rm)

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
    # embedding_pipeline("localhost", 6333)
    selected_topic = default_topic
    article_url = default_article_url
    run_storm(selected_topic, article_url)

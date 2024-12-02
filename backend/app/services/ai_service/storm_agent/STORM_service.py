import sys
from argparse import ArgumentParser
from os import PathLike

import knowledge_storm
from jinja2.utils import Namespace
from knowledge_storm import (
    STORMWikiLMConfigs,
    STORMWikiRunner,
    STORMWikiRunnerArguments,
)
from knowledge_storm.lm import OpenAIModel
from knowledge_storm.rm import TavilySearchRM

from backend.app.core.config import settings

sys.stdout.reconfigure(encoding="utf-8")


def storm_retrieval(args: Namespace, selected_topic: str, article_url: str) -> None:
    lm_configs = STORMWikiLMConfigs()
    openai_kwargs = {
        "api_key": settings.LITE_LLM_KEY,
        "api_base": "http://147.175.151.44/",
        "temperature": 1.0,
        "top_p": 0.9,
    }
    # STORM is a LM system so different components can be powered by different models to reach a good balance between cost and quality.
    # For a good practice, choose a cheaper/faster model for `conv_simulator_lm` which is used to split queries, synthesize answers in the conversation.
    # Choose a more powerful model for `article_gen_lm` to generate verifiable text with citations.
    gpt_4o_mini_mode = OpenAIModel(
        model="gpt-4o-mini", max_tokens=3000, **openai_kwargs
    )

    lm_configs.set_conv_simulator_lm(gpt_4o_mini_mode)
    lm_configs.set_question_asker_lm(gpt_4o_mini_mode)
    lm_configs.set_outline_gen_lm(gpt_4o_mini_mode)
    lm_configs.set_article_gen_lm(gpt_4o_mini_mode)
    lm_configs.set_article_polish_lm(gpt_4o_mini_mode)

    # Check out the STORMWikiRunnerArguments class for more configurations.
    engine_args = STORMWikiRunnerArguments(
        output_dir=args.output_dir,
        max_conv_turn=args.max_conv_turn,
        max_perspective=args.max_perspective,
        search_top_k=args.search_top_k,
        max_thread_num=args.max_thread_num,
    )

    rm = TavilySearchRM(
        tavily_search_api_key=settings.TAVILY_API_KEY,
        k=engine_args.search_top_k,
        include_raw_content=True,
    )

    runner = STORMWikiRunner(engine_args, lm_configs, rm)

    topic = selected_topic
    runner.run(
        topic=topic,
        ground_truth_url=article_url,
        do_research=args.do_research,
        do_generate_outline=args.do_generate_outline,
        do_generate_article=args.do_generate_article,
        do_polish_article=args.do_polish_article,
    )
    runner.post_run()
    runner.summary()


def storm_agent(args: Namespace, selected_topic: str, article_url: str) -> None:
    monkey_patch_storm()

    storm_retrieval(args, selected_topic, article_url)


def setup_storm_parser() -> ArgumentParser:
    parser = ArgumentParser()
    # global arguments
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./results",
        help="Directory to store the outputs.",
    )
    parser.add_argument(
        "--max-thread-num",
        type=int,
        default=3,
        help="Maximum number of threads to use. The information seeking part and the article generation"
        "part can speed up by using multiple threads. Consider reducing it if keep getting "
        '"Exceed rate limit" error when calling LM API.',
    )
    # stage of the pipeline
    parser.add_argument(
        "--do-research",
        action="store_true",
        help="If True, simulate conversation to research the topic; otherwise, load the results.",
    )
    parser.add_argument(
        "--do-generate-outline",
        action="store_true",
        help="If True, generate an outline for the topic; otherwise, load the results.",
    )
    parser.add_argument(
        "--do-generate-article",
        action="store_true",
        help="If True, generate an article for the topic; otherwise, load the results.",
    )
    parser.add_argument(
        "--do-polish-article",
        action="store_true",
        help="If True, polish the article by adding a summarization section and (optionally) removing "
        "duplicate content.",
    )
    # hyperparameters for the pre-writing stage
    parser.add_argument(
        "--max-conv-turn",
        type=int,
        default=3,
        help="Maximum number of questions in conversational question asking.",
    )
    parser.add_argument(
        "--max-perspective",
        type=int,
        default=3,
        help="Maximum number of perspectives to consider in perspective-guided question asking.",
    )
    parser.add_argument(
        "--search-top-k",
        type=int,
        default=3,
        help="Top k search results to consider for each search query.",
    )
    # hyperparameters for the writing stage
    parser.add_argument(
        "--retrieve-top-k",
        type=int,
        default=3,
        help="Top k collected references for each section title.",
    )
    parser.add_argument(
        "--remove-duplicate",
        action="store_true",
        help="If True, remove duplicate content from the article.",
    )

    return parser


# STORM file writing util method does not have utf-8 encoding
# Therefore monkey-patch is needed to prevent from crashing when in writing slovak language
def file_write_utf8(
    s: str, path: int | str | bytes | PathLike[str] | PathLike[bytes]
) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def monkey_patch_storm() -> None:
    knowledge_storm.utils.FileIOHelper.write_str = file_write_utf8

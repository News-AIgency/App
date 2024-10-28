from pydantic import BaseModel


class TestLiteLLMPoem(BaseModel):
    poem: str


class TopicsResponse(BaseModel):
    chain_of_thought: str
    topics: list[str]


class ArticleResponse(BaseModel):
    headlines: list[str]
    perex: str
    article: str

from pydantic import BaseModel


class TopicsResponse(BaseModel):
    chain_of_thought: str
    topics: list[str]

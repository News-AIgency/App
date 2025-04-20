from collections.abc import AsyncGenerator
from typing import Annotated

import models
import uvicorn
from database import Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# models.Base.metadata.create_all(bind=engine)


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: list[ChoiceBase]


class GeneratedArticle(BaseModel):
    url: "Sources"
    heading: "Heading"
    topic: "Topic"
    text: "Text"
    body: "Body"
    perex: "Perex"
    tags: list["Tags"]
    # images: Optional[list["Images"]] = []

    class Config:
        arbitraty_types_allowed = True


class Sources(BaseModel):
    url: str

    class Config:
        arbitrary_types_allowed = True


class Heading(BaseModel):
    heading_content: str

    class Config:
        arbitraty_types_allowed = True


class Topic(BaseModel):
    topic_content: str

    class Config:
        arbitraty_types_allowed = True


class Text(BaseModel):
    text_content: str

    class Config:
        arbitraty_types_allowed = True


class Body(BaseModel):
    body_content: str

    class Config:
        arbitraty_types_allowed = True


class Perex(BaseModel):
    perex_content: str

    class Config:
        arbitraty_types_allowed = True


class Tags(BaseModel):
    tags_content: str

    class Config:
        arbitraty_types_allowed = True


class Images(BaseModel):
    images_content: str

    class Config:
        arbitraty_types_allowed = True


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@app.post("/save_article/")  # , status_code=status.HTTP_201_CREATED
async def save_article(article: GeneratedArticle, db: db_dependency) -> dict:
    try:
        url = models.Sources(url=article.url.url)
        heading = models.Heading(heading_content=article.heading.heading_content)
        topic = models.Topic(topic_content=article.topic.topic_content)
        perex = models.Perex(perex_content=article.perex.perex_content)
        body = models.Body(body_content=article.body.body_content)
        text = models.Text(text_content=article.text.text_content)

        print(type(heading), type(topic), type(perex), type(body), type(text))
        db.add(url)
        db.add(heading)
        db.add(topic)
        db.add(perex)
        db.add(body)
        db.add(text)
        await db.commit()
        await db.refresh(url)
        await db.refresh(heading)
        await db.refresh(topic)
        await db.refresh(perex)
        await db.refresh(body)
        await db.refresh(text)

        tag_ids = []
        for tag_data in article.tags:
            tag = models.Tags(tags_content=tag_data.tags_content)
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
            tag_ids.append(tag)

        new_article = models.GeneratedArticles(
            heading=heading,
            topic=topic,
            text=text,
            body=body,
            perex=perex,
            sources=url,
        )
        new_article.tags.extend(tag_ids)

        db.add(new_article)
        await db.commit()
        await db.refresh(new_article)

        return {"id": new_article.id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

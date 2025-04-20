from collections.abc import AsyncGenerator
from typing import Annotated, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

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


#class ChoiceBase(BaseModel):
    #   choice_text: str
    #is_correct: bool


#class QuestionBase(BaseModel):
    #   question_text: str
    #choices: list[ChoiceBase]


class GeneratedArticle(BaseModel):
    url: "Sources"
    heading: "Heading"
    topic: "Topic"
   # text: "Text"
    body: "Body"
    perex: "Perex"
    engaging_text: "EngagingText"
    tags: list["Tags"]
    graph_data: "GraphData"
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


# class Text(BaseModel):
#     text_content: str
#
#     class Config:
#         arbitraty_types_allowed = True


class Body(BaseModel):
    body_content: str

    class Config:
        arbitraty_types_allowed = True


class Perex(BaseModel):
    perex_content: str

    class Config:
        arbitraty_types_allowed = True

class EngagingText(BaseModel):
    engaging_text_content: str
    class Config:
        arbitraty_types_allowed = True


class Tags(BaseModel):
    tags_content: str

    class Config:
        arbitraty_types_allowed = True

class GraphData(BaseModel):
    graph_type: Optional[str] = None
    graph_labels: Optional[list[str]] = None
    graph_values: Optional[list[float]] = None

    class Config:
        arbitraty_types_allowed = True


class Images(BaseModel):
    images_content: str

    class Config:
        arbitraty_types_allowed = True


class Test(BaseModel):
    test: str

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
        engaging_text = models.EngagingText(engaging_text_content=article.engaging_text.engaging_text_content)
        #tags are handled lower, dont add them here
        #graph_type = models.GraphData(graph_type=article.graph_type.graph_type)
        #graph_labels = models.GraphData(graph_labels=article.graph_labels.graph_labels)
        #graph_values = models.GraphData(graph_values=article.graph_values.graph_values)
        if article.graph_data:
            graph_data = models.GraphData(
                graph_type=article.graph_data.graph_type,
                graph_labels=article.graph_data.graph_labels,
                graph_values=article.graph_data.graph_values
            )
            db.add(graph_data)

        #print(type(heading), type(topic), type(perex), type(body), type(text))
        db.add(url)
        db.add(heading)
        db.add(topic)
        db.add(perex)
        db.add(body)
        db.add(engaging_text)
        await db.commit()
        await db.refresh(url)
        await db.refresh(heading)
        await db.refresh(topic)
        await db.refresh(perex)
        await db.refresh(body)

        tag_ids = []
        for tag_data in article.tags:
            tag = models.Tags(tags_content=tag_data.tags_content)
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
            tag_ids.append(tag)

        new_article = models.GeneratedArticles(
            heading=heading,
            engaging_text=engaging_text,
            perex=perex,
            body=body,
            graph_data=graph_data,
            topic=topic,
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

@app.get("/articles/{generated_article_id}")
async def get_articles(generated_article_id: int, db: db_dependency):
    try:
        result = await db.execute(
            select(models.GeneratedArticles)
            .options(
                selectinload(models.GeneratedArticles.heading),
                selectinload(models.GeneratedArticles.topic),
                selectinload(models.GeneratedArticles.body),
                selectinload(models.GeneratedArticles.perex),
                selectinload(models.GeneratedArticles.tags),
                selectinload(models.GeneratedArticles.sources),
                selectinload(models.GeneratedArticles.engaging_text),
                selectinload(models.GeneratedArticles.graph_data),
            )
            .where(models.GeneratedArticles.id == generated_article_id)
        )
        article = result.scalars().first()

        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        return {
            "id": article.id,
            "url": article.sources.url,
            "heading": article.heading.heading_content,
            "topic": article.topic.topic_content,
            "body": article.body.body_content,
            "perex": article.perex.perex_content,
            "engaging_text": article.engaging_text.engaging_text_content,
            "tags": [tag.tags_content for tag in article.tags],
            "graph_type": article.graph_data.graph_type,
            "graph_labels": article.graph_data.graph_labels,
            "graph_values": article.graph_data.graph_values,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch article: {str(e)}")

@app.patch("/articles/{article_id}")
async def update_article(
    article_id: int,
    update_data: UpdateArticleRequest,
    db: db_dependency
):
    try:
        result = await db.execute(
            select(models.GeneratedArticles)
            .options(
                selectinload(models.GeneratedArticles.heading),
                selectinload(models.GeneratedArticles.engaging_text),
                selectinload(models.GeneratedArticles.perex),
                selectinload(models.GeneratedArticles.body),
                selectinload(models.GeneratedArticles.tags),
            )
            .where(models.GeneratedArticles.id == article_id)
        )

        article = result.scalars().first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

       
        if update_data.heading and article.headings_id:
            heading_obj = await db.get(models.Heading, article.headings_id)
            if heading_obj:
                heading_obj.heading_content = update_data.heading

        if update_data.engaging_text and article.engaging_text_id:
            engaging_obj = await db.get(models.EngagingText, article.engaging_text_id)
            if engaging_obj:
                engaging_obj.engaging_text_content = update_data.engaging_text

        if update_data.perex and article.perex_id:
            perex_obj = await db.get(models.Perex, article.perex_id)
            if perex_obj:
                perex_obj.perex_content = update_data.perex

        if update_data.body and article.body_id:
            body_obj = await db.get(models.Body, article.body_id)
            if body_obj:
                body_obj.body_content = update_data.body


        if update_data.tags is not None:
            await db.refresh(article, attribute_names=["tags"])  

            existing_tag_contents = {tag.tags_content for tag in article.tags}


            for tag_content in update_data.tags:
                if tag_content not in existing_tag_contents:
                    new_tag = models.Tags(tags_content=tag_content)
                    db.add(new_tag)
                    article.tags.append(new_tag)


            for tag in list(article.tags):
                if tag.tags_content not in update_data.tags:
                    article.tags.remove(tag)

        await db.commit()
        return {"message": "Article updated successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

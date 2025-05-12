from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.db import models
from backend.app.db.database import Base, db_manager

# app = FastAPI()
router = APIRouter()


@router.on_event("startup")
async def startup_event() -> None:
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# models.Base.metadata.create_all(bind=engine)


# class ChoiceBase(BaseModel):
#   choice_text: str
# is_correct: bool


# class QuestionBase(BaseModel):
#   question_text: str
# choices: list[ChoiceBase]


class GeneratedArticle(BaseModel):
    url: "Sources"
    heading: "Heading"
    topic: "Topic"
    # text: "Text"
    body: "Body"
    perex: "Perex"
    engaging_text: "EngagingText"
    tags: list["Tags"]
    graph_data: Optional["GraphData"] = None
    # images: Optional[list["Images"]] = []

    class Config:
        arbitrary_types_allowed = True


class Sources(BaseModel):
    url: str

    class Config:
        arbitrary_types_allowed = True


class Heading(BaseModel):
    heading_content: str

    class Config:
        arbitrary_types_allowed = True


class Topic(BaseModel):
    topic_content: str

    class Config:
        arbitrary_types_allowed = True


# class Text(BaseModel):
#     text_content: str
#
#     class Config:
#         arbitraty_types_allowed = True


class Body(BaseModel):
    body_content: str

    class Config:
        arbitrary_types_allowed = True


class Perex(BaseModel):
    perex_content: str

    class Config:
        arbitrary_types_allowed = True


class EngagingText(BaseModel):
    engaging_text_content: str

    class Config:
        arbitrary_types_allowed = True


class Tags(BaseModel):
    tags_content: str

    class Config:
        arbitrary_types_allowed = True


class GraphData(BaseModel):
    graph_type: Optional[str] = None
    graph_labels: Optional[list[str]] = None
    graph_values: Optional[list[float]] = None
    gen_graph: Optional[bool] = None
    graph_title: Optional[str] = None
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    #graph_axis_labels: Optional[dict[str, Optional[str]]] = None  # e.g., {'x_axis': 'Time', 'y_axis': 'Value'}

    class Config:
        arbitrary_types_allowed = True


class Images(BaseModel):
    images_content: str

    class Config:
        arbitrary_types_allowed = True


class Test(BaseModel):
    test: str

    class Config:
        arbitrary_types_allowed = True


class UpdateArticleRequest(BaseModel):
    heading: Optional[str] = None
    engaging_text: Optional[str] = None
    perex: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[list[str]] = None


db_dependency = Annotated[AsyncSession, Depends(db_manager.get_db)]


@router.post("/save_article/")
async def save_article(article: GeneratedArticle, db: db_dependency) -> dict:
    try:
        url = models.Sources(url=article.url.url)
        heading = models.Heading(heading_content=article.heading.heading_content)
        topic = models.Topic(topic_content=article.topic.topic_content)
        perex = models.Perex(perex_content=article.perex.perex_content)
        body = models.Body(body_content=article.body.body_content)
        engaging_text = models.EngagingText(engaging_text_content=article.engaging_text.engaging_text_content)

        graph_data = None
        if article.graph_data:

            graph_fields = {}
            if article.graph_data.gen_graph is not None:
                graph_fields["gen_graph"] = article.graph_data.gen_graph
            if article.graph_data.graph_title is not None:
                graph_fields["graph_title"] = article.graph_data.graph_title
            if article.graph_data.graph_type is not None:
                graph_fields["graph_type"] = article.graph_data.graph_type
            if article.graph_data.graph_labels is not None:
                graph_fields["graph_labels"] = article.graph_data.graph_labels
            if article.graph_data.graph_values is not None:
                graph_fields["graph_values"] = article.graph_data.graph_values
            if article.graph_data.x_axis is not None:
                graph_fields["x_axis"] = article.graph_data.x_axis
            if article.graph_data.y_axis is not None:
                graph_fields["y_axis"] = article.graph_data.y_axis
            #if article.graph_data.graph_axis_labels is not None:
             #   graph_fields["graph_axis_labels"] = article.graph_data.graph_axis_labels

            # Only add if there's at least something to store
            if graph_fields:
                graph_data = models.GraphData(**graph_fields)
                db.add(graph_data)



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
        if graph_data:
            await db.refresh(graph_data)
        await db.refresh(engaging_text)

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



@router.get("/articles/{generated_article_id}")
async def get_articles(generated_article_id: int, db: db_dependency) -> dict[str, Any]:
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

        graph_data = article.graph_data
        return {
            "id": article.id,
            "url": article.sources.url,
            "heading": article.heading.heading_content,
            "topic": article.topic.topic_content,
            "body": article.body.body_content,
            "perex": article.perex.perex_content,
            "engaging_text": article.engaging_text.engaging_text_content,
            "tags": [tag.tags_content for tag in article.tags],
            "graph_data": {
                "graph_type": graph_data.graph_type,
                "graph_labels": graph_data.graph_labels,
                "graph_values": graph_data.graph_values,
                "gen_graph": graph_data.gen_graph,
                "graph_title": graph_data.graph_title,
                "x_axis": graph_data.x_axis,
                "y_axis": graph_data.y_axis,
            } if graph_data else None
        }


    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch article: {str(e)}"
        )



@router.patch("/articles/{article_id}")
async def update_article(
    article_id: int, update_data: UpdateArticleRequest, db: db_dependency
) -> dict[str, str]:
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
            await db.refresh(
                article, attribute_names=["tags"]
            )  # Ensures tags are eagerly loaded

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
    pass
#   uvicorn.run(router, host="0.0.0.0", port=8002)

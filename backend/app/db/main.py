from typing import Annotated, Optional, AsyncGenerator

import models
import uvicorn
from database import Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
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
    heading: "Heading"
    topic: "Topic"
    text: "Text"
    body: "Body"
    perex: "Perex"
    tags: list["Tags"]
    images: Optional[list["Images"]] = []

    class Config:
        arbitraty_types_allowed = True


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


# async def get_db():
#   async with SessionLocal as session:
#  db = SessionLocal()
# try:
#    yield db
# finally:
#   db.close()

#  async def get_db():
# async with SessionLocal() as session:
#   yield session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@app.post("/save_article/", status_code=status.HTTP_201_CREATED)
async def save_article(article: GeneratedArticle, db: db_dependency) -> None:
    try:
        """heading = models.Heading(heading_content=article.heading.heading_content)
        topic = models.Topic(topic_content=article.topic.topic_content)
        perex = models.Perex(perex_content=article.perex.perex_content)
        body = models.Body(body_content=article.body.body_content)
        text = models.Text(text_content=article.text.text_content)

        print(type(heading), type(topic), type(perex), type(body), type(text))
        db.add(heading)
        db.add(topic)
        db.add(perex)
        db.add(body)
        db.add(text)
        print("KOASDK")
        db.commit()
        print("GELLO")
        db.refresh(heading)
        db.refresh(topic)
        db.refresh(perex)
        db.refresh(body)
        db.refresh(text)

        tag_entries = [models.Tags(tags_content=tag.tags_content) for tag in article.tags]
        print("SUHAJ")
        db.add_all(tag_entries)
        db.commit()
        print("estok")
        for tag in tag_entries:
            db.refresh(tag)
        print(heading.id, topic.id, text.id, body.id, perex.id, tag_entries[0].id)
        new_article = models.GeneratedArticles(
            heading=heading.id,
            topic=topic.id,
            text=text.id,
            body=body.id,
            perex=perex.id,
            tags=tag_entries[0].id if tag_entries else None,
        )
        print("KOSMODROM")
        #db.add(new_article)
        db.commit()
        #db.refresh(new_article)
        print("SCHEISE")
        return {"id": new_article.id}"""

        kon = models.Topic(topic_content="ALLAHU AKBAR")
        db.add(kon)
        db.commit()
        db.refresh(kon)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency) -> None:

    # dostali sme json
    # heading = models.XXX(json)
    # db.add(models.JSON)

    # heading = json
    # heading = models.XXX
    # db.
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)
    db.commit()


@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency) -> None:
    result = (
        db.query(models.Questions).filter(models.Questions.id == question_id).first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result


@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency) -> None:
    result = (
        db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

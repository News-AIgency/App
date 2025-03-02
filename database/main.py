from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import engine, SessionLocal

import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class HeadingBase(BaseModel):
    heading_content: str

class HeadingCreate(HeadingBase):
    generated_article_id: int

class Heading(HeadingBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Topic Schema ###
class TopicBase(BaseModel):
    topic_content: str

class TopicCreate(TopicBase):
    generated_article_id: int

class Topic(TopicBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Text Schema ###
class TextBase(BaseModel):
    text_content: str

class TextCreate(TextBase):
    generated_article_id: int

class Text(TextBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Body Schema ###
class BodyBase(BaseModel):
    body_content: str

class BodyCreate(BodyBase):
    generated_article_id: int

class Body(BodyBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Perex Schema ###
class PerexBase(BaseModel):
    perex_content: str

class PerexCreate(PerexBase):
    generated_article_id: int

class Perex(PerexBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Tags Schema ###
class TagsBase(BaseModel):
    tag_content: str

class TagsCreate(TagsBase):
    generated_article_id: int

class Tags(TagsBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Images Schema ###
class ImagesBase(BaseModel):
    link_to_image: str

class ImagesCreate(ImagesBase):
    generated_article_id: int

class Images(ImagesBase):
    id: int
    generated_article_id: int

    class Config:
        from_attributes = True


### Generated Article Schema (Nested Relationships) ###
class GeneratedArticleBase(BaseModel):
    pass  # No fields because it references other models

class GeneratedArticleCreate(BaseModel):
    heading: HeadingCreate
    topic: TopicCreate
    text: TextCreate
    body: BodyCreate
    perex: PerexCreate
    tags: TagsCreate
    images: ImagesCreate

class GeneratedArticle(GeneratedArticleBase):
    id: int
    heading: Heading
    topic: Topic
    text: Text
    body: Body
    perex: Perex
    tags: Tags
    images: Images

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result

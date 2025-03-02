from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))

class GeneratedArticles(Base):
    __tablename__ = 'generated_articles'
    id = Column(Integer, primary_key=True, index=True)

    heading = relationship("Heading", backref="generated_articles")
    topic = relationship("Topic", backref="generated_articles")
    text = relationship("Text", backref="generated_articles")
    body = relationship("Body", backref="generated_articles")
    perex = relationship("Perex", backref="generated_articles")
    tags = relationship("Tags", backref="generated_articles")
    images = relationship("Images", backref="generated_articles")
#     sources_id = Column(Integer, ForeignKey('sources.id'))


class Heading(Base):
    __tablename__ = 'headings'
    id = Column(Integer, primary_key=True, index=True)
    heading_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True, index=True)
    topic_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Text(Base):
    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True, index=True)
    text_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Body(Base):
    __tablename__ = 'body'
    id = Column(Integer, primary_key=True, index=True)
    body_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Perex(Base):
    __tablename__ = 'perex'
    id = Column(Integer, primary_key=True, index=True)
    perex_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    tag_content = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))

class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    link_to_image = Column(String, index=True)
    generated_article_id = Column(Integer, ForeignKey('generated_articles.id'))


#
# class Sources(Base):
#     __tablename__ = 'sources'
#     id = Column(Integer, primary_key=True, index=True)
#     source = Column(String, index=True)
#     generated_articles = relationship("GeneratedArticles", backref="sources")
#     scraped_article_id = Column(Integer, ForeignKey('scraped_articles.id'))
#     scraped_article = relationship("ScrapedArticles", back_populates="sources", uselist=False)
#
#
# class ScrapedArticles(Base):
#     __tablename__ = 'scraped_articles'
#     id = Column(Integer, primary_key=True, index=True)
#     article_content = Column(String, index=True)
#     article_source = relationship("Sources", back_populates="scraped_articles")


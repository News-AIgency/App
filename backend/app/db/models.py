from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from database import Base


article_tags = Table(
    "article_tags",
    Base.metadata,
    Column(
        "article_id", Integer, ForeignKey("generated_articles.id"), primary_key=True
    ),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class GeneratedArticles(Base):
    __tablename__ = "generated_articles"
    id = Column(Integer, primary_key=True, index=True)

    headings_id = Column(Integer, ForeignKey("headings.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
   # text_id = Column(Integer, ForeignKey("texts.id"), nullable=True)
    body_id = Column(Integer, ForeignKey("body.id"), nullable=True)
    perex_id = Column(Integer, ForeignKey("perex.id"), nullable=True)
    engaging_text_id = Column(Integer, ForeignKey("engaging_texts.id"), nullable=True)
    graph_data_id = Column(Integer, ForeignKey("graph_data.id"), nullable=True)
    tags_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    # images_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    sources_id = Column(Integer, ForeignKey("sources.id"), nullable=True)

    heading = relationship("Heading",back_populates="article", foreign_keys=[headings_id])
    topic = relationship("Topic", back_populates="article", foreign_keys=[topic_id])
   # text = relationship("Text", back_populates="article", foreign_keys=[text_id])
    body = relationship("Body", back_populates="article", foreign_keys=[body_id])
    perex = relationship("Perex", back_populates="article", foreign_keys=[perex_id])
    tags = relationship("Tags", secondary=article_tags, back_populates="article")
    engaging_text = relationship("EngagingText", back_populates="article", foreign_keys=[engaging_text_id])
    graph_data = relationship("GraphData", back_populates="article", foreign_keys=[graph_data_id])
    # images = relationship("Images", back_populates="article", foreign_keys=[images_id])
    sources = relationship(
        "Sources", back_populates="article", foreign_keys=[sources_id]
    )


class Sources(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="sources",
        foreign_keys=[GeneratedArticles.sources_id],
    )


class Heading(Base):
    __tablename__ = "headings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    heading_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="heading",
        foreign_keys=[GeneratedArticles.headings_id],
    )

class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tags_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="tags",
        foreign_keys=[GeneratedArticles.tags_id],
    )


class EngagingText(Base):
    __tablename__ = "engaging_texts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    engaging_text_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="engaging_text",
        foreign_keys=[GeneratedArticles.engaging_text_id],
    )


class Topic(Base):

    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="topic",
        foreign_keys=[GeneratedArticles.topic_id],
    )


# class Text(Base):
#     __tablename__ = "texts"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     text_content = Column(String, index=True, nullable=False)
#     article = relationship(
#         "GeneratedArticles",
#         back_populates="text",
#         foreign_keys=[GeneratedArticles.text_id],
#     )


class Body(Base):
    __tablename__ = "body"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="body",
        foreign_keys=[GeneratedArticles.body_id],
    )


class Perex(Base):
    __tablename__ = "perex"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    perex_content = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="perex",
        foreign_keys=[GeneratedArticles.perex_id],
    )

class GraphData(Base):
    __tablename__ = "graph_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #does_graph_exist = Column(Boolean, index=True, nullable=False)
    graph_type = Column(String, index=True, nullable=False)
    graph_labels = Column(JSON, nullable=False)
    graph_values = Column(JSON, nullable=False)

    article = relationship(
        "GeneratedArticles",
        back_populates="graph_data",
        uselist=False
    )



"""class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link_to_image = Column(String, index=True, nullable=False)
    article = relationship(
        "GeneratedArticles",
        back_populates="images",
        foreign_keys=[GeneratedArticles.images_id],
    )"""


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

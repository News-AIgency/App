from fastapi import APIRouter

from backend.app.api.routes import grammar_checker, topic_to_article, url_to_topic

api_router = APIRouter()
api_router.include_router(url_to_topic.router)
api_router.include_router(topic_to_article.router)
api_router.include_router(grammar_checker.router)

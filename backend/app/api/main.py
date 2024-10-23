from fastapi import APIRouter

from backend.app.api.routes import url_to_topic

api_router = APIRouter()
api_router.include_router(url_to_topic.router)

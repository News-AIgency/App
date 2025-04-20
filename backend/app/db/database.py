from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

user = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
database = settings.POSTGRES_DB
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_PORT = settings.POSTGRES_PORT

# print(user)
# print(password)p
# print(database)

URL_DATABASE = f"postgresql+asyncpg://{user}:{password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{database}"  # the actual database
# #URL_DATABASE = "postgresql+asyncpg://postgres:kubko123@localhost/new_db" # local testing database
engine = create_async_engine(URL_DATABASE)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()

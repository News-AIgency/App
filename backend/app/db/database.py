import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
database = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

#print(user)
#print(password)p
#print(database)

URL_DATABASE = f"postgresql+asyncpg://{user}:{password}@{POSTGRES_HOST}:15432/{database}" #the actual database
#URL_DATABASE = "postgresql+asyncpg://postgres:kubko123@localhost/new_db" # local testing database
engine = create_async_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


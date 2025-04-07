from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = "postgresql+asyncpg://[user]:[password]@localhost/[database name]"
engine = create_async_engine(URL_DATABASE)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()

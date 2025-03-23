from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL_DATABASE = "postgresql://[user]:[password]@localhost/[database name]"
URL_DATABASE = "postgresql+asyncpg://postgres:1234@localhost/testdb"
engine = create_async_engine(URL_DATABASE)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()

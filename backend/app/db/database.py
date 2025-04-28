from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.app.core.config import settings

Base = declarative_base()


class DatabaseManager:
    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.SessionLocal: Optional[sessionmaker] = None

    def get_database_url(self) -> str:
        user = settings.POSTGRES_USER
        password = settings.POSTGRES_PASSWORD
        database = settings.POSTGRES_DB
        host = settings.POSTGRES_HOST
        port = settings.POSTGRES_PORT
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

    def start(self) -> None:
        if self.engine is None:
            database_url = self.get_database_url()
            self.engine = create_async_engine(database_url, echo=False)

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=AsyncSession,
            )

    async def stop(self) -> None:
        if self.engine is not None:
            await self.engine.dispose()

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        if self.SessionLocal is None:
            raise RuntimeError(
                "Database session not initialized. Did you call start()?"
            )

        async with self.SessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()


db_manager = DatabaseManager()

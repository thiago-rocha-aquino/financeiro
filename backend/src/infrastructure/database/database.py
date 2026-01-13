from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.config import get_settings


class Database:
    """Gerenciador de conexão com o banco de dados."""

    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(
            database_url,
            echo=False,
            future=True,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def create_tables(self) -> None:
        from src.infrastructure.database.models import Base

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        from src.infrastructure.database.models import Base

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


_database: Database | None = None


def get_database() -> Database:
    global _database
    if _database is None:
        settings = get_settings()
        _database = Database(settings.database_url)
    return _database


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    database = get_database()
    async for session in database.get_session():
        yield session

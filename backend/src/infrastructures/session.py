from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
import structlog
from collections.abc import AsyncIterator

from backend.src.config.base import Settings
# import backend.src.infrastructures.binders.bind1

logger = structlog.get_logger(__name__)

def create_engine(url: str, is_echo: bool = True) -> AsyncEngine:
    """
    Create an asynchronous  SQLAlchemy engine.

    :param url: The database connection URL.
    :param is_echo: If True, SQL statements will be echoed to the console.
    :return: An AsyncEngine instance.
    """

    return create_async_engine(
        url=url,
        echo=is_echo,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={}
    )


def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Create an asynchronous sessionmaker for SQLAlchemy engine.

    :param engine: The AsyncEngine instance.
    :return: An async_sessionmaker configured for AsyncSession.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

class DatabaseProvider:
    """
    Предоставляет зависимости, связанные с базой данных, такие как session factory и сеансы.
    """
    engine: AsyncEngine

    @classmethod
    async def get_session_factory(
        cls, settings: Settings
    ) -> async_sessionmaker[AsyncSession]:
        """
        Предоставляет фабрику асинхронных сеансов для SQLAlchemy.
        """
        cls.engine = create_engine(str(settings.database_url), is_echo=settings.debug)
        session_factory = get_session_factory(cls.engine)
        try:
            return session_factory
        finally:
            await cls.engine.dispose()

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        return cls.engine

    @classmethod
    async def get_session(
        cls
    ) -> AsyncIterator[AsyncSession]:
        """
        Обеспечивает асинхронный сеанс SQLAlchemy.
        """
        async with (await cls.get_session_factory(Settings()))() as session:
            while True:
                yield session


async def get_session(session_generator: AsyncIterator[AsyncSession] = DatabaseProvider.get_session()) -> AsyncSession:
    return await anext(session_generator)

from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.infrastructures.models.base import Base
from backend.src.infrastructures.session import DatabaseProvider



@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DBSQLAlchemy:
    """
    Реализация репозитория работы с базой данных на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    """

    @classmethod
    async def setup_db(
            cls,
            session: AsyncSession,
    ) -> None:
        """
        Обнуляет базу данных.

        :param session:
        :return:
        """
        async with DatabaseProvider.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


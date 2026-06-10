import logging
from dataclasses import dataclass
from typing import final

from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.infrastructures.session import get_session

from backend.src.infrastructures.repositories.example import ExampleRepositoriesSQLAlchemy

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=False, slots=True, kw_only=True)
class UnitOfWorkSQLAlchemy:
    """
    SQLAlchemy реализует шаблон Unit of Work.

    Этот класс координирует транзакции с базой данных и предоставляет доступ к репозиториям.
    Использует типы протоколов вместо конкретных реализаций для лучшей тестируемости
    и соблюдения принципа инверсии зависимостей.
    """

    session: AsyncSession = None
    repository: ExampleRepositoriesSQLAlchemy = ExampleRepositoriesSQLAlchemy

    async def __aenter__(self) -> AsyncSession:
        """
        Входит в диспетчер асинхронного контекста.
        :return: this UOW instance.
        """
        logger.debug("Starting database transaction")
        self.session = await get_session()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Завершает работу асинхронного контекстного менеджера.
        Фиксирует изменения, если не возникло исключения, в противном случае выполняет откат.
        """
        if exc_type is not None:
            logger.warning(
                "Transaction rolled back due to exception: %s - %s",
                exc_type.__name__,
                str(exc_val)
            )
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """
        Фиксирует текущую транзакцию в базе данных.
        """
        logger.debug("Committing transaction")
        await self.session.commit()
        logger.debug("Transaction committed successfully")

    async def rollback(self) -> None:
        """
        Откатывает текущую транзакцию в базе данных.
        """
        logger.debug("Rolling back transaction")
        await self.session.rollback()
        logger.debug("Transaction rolled back successfully")
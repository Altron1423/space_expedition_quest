from typing import TYPE_CHECKING

import structlog

# from backend.src.application.dtos.user import UserDTO
# from backend.src.application.mappers import UserMapper
from backend.src.infrastructures.repositories.db import DBSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

# if TYPE_CHECKING:
    # from backend.src.domain.entities.user import UserEntity

logger = structlog.get_logger(__name__)


class SetupDatabaseUseCase:
    uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
    # user_mapper: UserMapper = UserMapper()

    repository: DBSQLAlchemy = DBSQLAlchemy

    @classmethod
    async def SetupDatabase(cls) -> None:
        """
        Пересоздаёт базу данных.

        :return:
        """

        async with cls.uow as session:
            await cls.repository.setup_db(session)


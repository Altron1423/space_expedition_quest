from uuid import UUID

import structlog

from typing import TYPE_CHECKING

from backend.src.application.dtos.admin import CreateAdminDTO
from backend.src.application.exceptions import AdminAlreadyExistsError
from backend.src.application.mappers import CreateAdminMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.repositories.admin import AdminRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import AdminEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
admins_mapper: CreateAdminMapper = CreateAdminMapper()

repository: AdminRepositoriesSQLAlchemy = AdminRepositoriesSQLAlchemy()


async def CreateAdminInRepoUseCase(dto: CreateAdminDTO) -> UUID:
    """
    Выполняет сценарий для создания команды в хранилище.

    :return: None
    """
    async with uow as session:
        admin_entity = admins_mapper.to_entity(
            dto=dto
        )

        try:
            await repository.save(
                session=session,
                admin=admin_entity,
            )
        except RepositoryConflictError as exc:
            raise AdminAlreadyExistsError(
                f"Product '{admin_entity.unique_id}' already exists"
            ) from exc
    return admin_entity.unique_id

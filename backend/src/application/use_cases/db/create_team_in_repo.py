from uuid import UUID

import structlog

from typing import TYPE_CHECKING

from backend.src.application.dtos.team import CreateTeamDTO
from backend.src.application.exceptions import TeamAlreadyExistsError
from backend.src.application.mappers import CreateTeamMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.repositories.team import TeamRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import TeamEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
teams_mapper: CreateTeamMapper = CreateTeamMapper()

repository: TeamRepositoriesSQLAlchemy = TeamRepositoriesSQLAlchemy()


async def CreateTeamInRepoUseCase(dto: CreateTeamDTO) -> UUID:
    """
    Выполняет сценарий для создания команды в хранилище.

    :return: None
    """
    async with uow as session:
        team_entity = teams_mapper.to_entity(
            dto=dto
        )

        try:
            await repository.save(
                session=session,
                team=team_entity,
            )
        except RepositoryConflictError as exc:
            raise TeamAlreadyExistsError(
                f"Product '{team_entity.unique_id}' already exists"
            ) from exc
    return team_entity.unique_id

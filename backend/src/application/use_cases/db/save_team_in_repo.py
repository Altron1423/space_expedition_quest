from uuid import UUID

import structlog

from backend.src.application.dtos.team import TeamDTO
from backend.src.application.exceptions import TeamAlreadyExistsError
from backend.src.application.mappers import TeamMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.repositories.team import TeamRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy


logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
teams_mapper: TeamMapper = TeamMapper()

repository: TeamRepositoriesSQLAlchemy = TeamRepositoriesSQLAlchemy()


async def SaveTeamInRepoUseCase(dto: TeamDTO) -> UUID:
    """
    Выполняет сценарий для сохранения команды в хранилище.

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
                f"Team '{team_entity.unique_id}' already exists"
            ) from exc
    return team_entity.unique_id

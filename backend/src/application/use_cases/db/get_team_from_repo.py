import structlog

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from backend.src.application.dtos.team import TeamDTO
from backend.src.application.mappers import TeamMapper
from backend.src.infrastructures.repositories.team import TeamRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import TeamEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
problems_mapper: TeamMapper = TeamMapper()

repository: TeamRepositoriesSQLAlchemy = TeamRepositoriesSQLAlchemy()


async def GetTeamsListFromRepoUseCase() -> list[TeamDTO]:
    """
    Выполняет сценарий для получения всех команд из хранилища.

    :return: list[TeamDTO], все найденные команды.
    """

    async with uow as session:
        problem_entities: list[TeamEntity] = await repository.get_list(session)
        if len(problem_entities) == 0:
            logger.info("Teams not found in repository")
        else:
            logger.info("Teams found in repository")
        return [
            problems_mapper.to_dto(problem_entity)
            for problem_entity in problem_entities
        ]

async def GetTeamByIdFromRepoUseCase(unique_id: UUID) -> Optional[TeamDTO]:
    """
    Выполняет сценарий для получения команды из хранилища.

    :return: TeamDTO, если она найдена в репозитории, в противном случае None.
    """

    async with uow as session:
        problem_entity: Optional[TeamEntity] = await repository.get_by_id(session, unique_id)
        if problem_entity:
            logger.info("Team found in repository")
        else:
            logger.info("Team not found in repository")
        return problem_entity

async def GetTeamByNameFromRepoUseCase(name: str) -> Optional[TeamDTO]:
    """
    Выполняет сценарий для получения команды из хранилища.

    :return: TeamDTO, если она найдена в репозитории, в противном случае None.
    """

    async with uow as session:
        problem_entity: Optional[TeamEntity] = await repository.get_by_name(session, name)
        if problem_entity:
            logger.info("Team found in repository")
        else:
            logger.info("Team not found in repository")
        return problem_entity


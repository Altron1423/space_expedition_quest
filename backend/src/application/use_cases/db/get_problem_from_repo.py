import structlog

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from backend.src.application.dtos.problem import ProblemDTO
from backend.src.application.mappers import ProblemMapper
from backend.src.infrastructures.repositories.problem import ProblemRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import ProblemEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
problems_mapper: ProblemMapper = ProblemMapper()

repository: ProblemRepositoriesSQLAlchemy = ProblemRepositoriesSQLAlchemy()


async def GetProblemsListFromRepoUseCase() -> list[ProblemDTO]:
    """
    Выполняет сценарий для всех задач из хранилища.

    :return: list[ProblemDTO], все найденные задачи.
    """

    async with uow as session:
        problem_entities: list[ProblemEntity] = await repository.get_list(session)
        if len(problem_entities) == 0:
            logger.info("Problems not found in repository")
        else:
            logger.info("Problems found in repository")
        return [
            problems_mapper.to_dto(problem_entity)
            for problem_entity in problem_entities
        ]

async def GetProblemByIdFromRepoUseCase(unique_id: UUID) -> Optional[ProblemDTO]:
    """
    Выполняет сценарий для получения задачи из хранилища.

    :return: ProblemDTO, если она найдена в репозитории, в противном случае None.
    """

    async with uow as session:
        problem_entity: Optional[ProblemEntity] = await repository.get_by_id(session, unique_id)
        if problem_entity:
            logger.info("Problem found in repository")
        else:
            logger.info("Problem not found in repository")
        return problem_entity

async def GetProblemByNameFromRepoUseCase(name: str) -> Optional[ProblemDTO]:
    """
    Выполняет сценарий для получения задачи из хранилища.

    :return: ProblemDTO, если она найдена в репозитории, в противном случае None.
    """

    async with uow as session:
        problem_entity: Optional[ProblemEntity] = await repository.get_by_name(session, name)
        if problem_entity:
            logger.info("Problem found in repository")
        else:
            logger.info("Problem not found in repository")
        return problem_entity


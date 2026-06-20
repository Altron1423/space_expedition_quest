import structlog

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from application.dtos.problem import ProblemDTO
from backend.src.domain.entities.problem import ProblemEntity
from backend.src.application.mappers import ProblemMapper
from backend.src.infrastructures.repositories.problem import ProblemRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import ProblemEntity

logger = structlog.get_logger(__name__)

class GetProblemFromRepoUseCase:
    uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
    problems_mapper: ProblemMapper = ProblemMapper()

    repository: ProblemRepositoriesSQLAlchemy = ProblemRepositoriesSQLAlchemy()

    @classmethod
    async def GetList(cls) -> list[ProblemDTO]:
        """
        Выполняет сценарий для всех задач из хранилища.

        :return: list[ProblemEntity], все найденные задачи.
        """

        async with cls.uow as session:
            problem_entities: list[ProblemEntity] = await cls.repository.get_list(session)
            if len(problem_entities) == 0:
                logger.info("Problems not found in repository")
            else:
                logger.info("Problems found in repository")
            return [
                cls.problems_mapper.to_dto(problem_entity)
                for problem_entity in problem_entities
            ]

    @classmethod
    async def GetById(cls, unique_id: UUID) -> Optional[ProblemDTO]:
        """
        Выполняет сценарий для получения задачи из хранилища.

        :return: ProblemEntity, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            problem_entity: Optional[ProblemEntity] = await cls.repository.get_by_id(session, unique_id)
            if problem_entity:
                logger.info("Problem found in repository")
                return cls.problems_mapper.to_dto(problem_entity)
            else:
                logger.info("Problem not found in repository")
                return None

    @classmethod
    async def GetByEvent_Stage(cls, unique_id: UUID, stage: int) -> list[ProblemDTO]:
        """
        Выполняет сценарий для получения задачи из хранилища.

        :return: ProblemEntity, если она найдена в репозитории, в противном случае None.
        """

        async with (cls.uow as session):
            problems_entity: list[ProblemEntity] = await cls.repository.get_by_event_stage(session, unique_id, stage)
            if problems_entity:
                logger.info("Problem found in repository")
            else:
                logger.info("Problem not found in repository")
            return [
                cls.problems_mapper.to_dto(problem_entity)
                for problem_entity in problems_entity
            ]


    @classmethod
    async def GetByName(cls, name: str) -> Optional[ProblemEntity]:
        """
        Выполняет сценарий для получения задачи из хранилища.

        :return: ProblemEntity, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            problem_entity: Optional[ProblemEntity] = await cls.repository.get_by_name(session, name)
            if problem_entity:
                logger.info("Problem found in repository")
            else:
                logger.info("Problem not found in repository")
            return problem_entity


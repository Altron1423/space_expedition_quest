import structlog

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from backend.src.application.dtos.team import TeamDTO
from backend.src.application.mappers import TeamMapper
from backend.src.infrastructures.repositories.admin import AdminRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import TeamEntity

logger = structlog.get_logger(__name__)

class GetAdminFromRepoUseCase:
    uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
    problems_mapper: TeamMapper = TeamMapper()

    repository: AdminRepositoriesSQLAlchemy = AdminRepositoriesSQLAlchemy()

    @classmethod
    async def GetList(cls) -> list[TeamDTO]:
        """
        Выполняет сценарий для получения всех команд из хранилища.

        :return: list[TeamDTO], все найденные команды.
        """

        async with cls.uow as session:
            problem_entities: list[TeamEntity] = await cls.repository.get_list(session)
            if len(problem_entities) == 0:
                logger.info("Teams not found in repository")
            else:
                logger.info("Teams found in repository")
            return [
                cls.problems_mapper.to_dto(problem_entity)
                for problem_entity in problem_entities
            ]


    @classmethod
    async def GetById(cls, unique_id: UUID) -> Optional[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            problem_entity: Optional[TeamEntity] = await cls.repository.get_by_id(session, unique_id)
            if problem_entity:
                logger.info("Team found in repository")
            else:
                logger.info("Team not found in repository")
            return problem_entity


    @classmethod
    async def GetByName(cls, name: str) -> Optional[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            problem_entity: Optional[TeamEntity] = await cls.repository.get_by_name(session, name)
            if problem_entity:
                logger.info("Team found in repository")
            else:
                logger.info("Team not found in repository")
            return problem_entity


    @classmethod
    async def GetByEmail(cls, email: str) -> Optional[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            problem_entity: Optional[TeamEntity] = await cls.repository.get_by_email(session, email)
            if problem_entity:
                logger.info("Team found in repository")
            else:
                logger.info("Team not found in repository")
            return problem_entity


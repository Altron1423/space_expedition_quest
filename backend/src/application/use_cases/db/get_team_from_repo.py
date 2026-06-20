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

class GetTeamFromRepoUseCase:
    uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
    teams_mapper: TeamMapper = TeamMapper()

    repository: TeamRepositoriesSQLAlchemy = TeamRepositoriesSQLAlchemy()

    @classmethod
    async def GetList(cls) -> list[TeamDTO]:
        """
        Выполняет сценарий для получения всех команд из хранилища.

        :return: list[TeamDTO], все найденные команды.
        """

        async with cls.uow as session:
            team_entities: list[TeamEntity] = await cls.repository.get_list(session)
            if len(team_entities) == 0:
                logger.info("Teams not found in repository")
            else:
                logger.info("Teams found in repository")
            return [
                cls.teams_mapper.to_dto(team_entity)
                for team_entity in team_entities
            ]

    @classmethod
    async def GetById(cls, unique_id: UUID) -> Optional[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            team_entity: Optional[TeamEntity] = await cls.repository.get_by_id(session, unique_id)
            if team_entity:
                logger.info("Team found in repository")
                return cls.teams_mapper.to_dto(team_entity)
            else:
                logger.info("Team not found in repository")
                return None

    @classmethod
    async def GetByEventID(cls, unique_id: UUID) -> list[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            teams_entity: list[TeamEntity] = await cls.repository.get_by_event_id(session, unique_id)
            if teams_entity:
                logger.info("Team found in repository")
            else:
                logger.info("Team not found in repository")
            return [
                cls.teams_mapper.to_dto(team_entity)
                for team_entity in teams_entity
            ]

    @classmethod
    async def GetByName(cls, name: str) -> Optional[TeamDTO]:
        """
        Выполняет сценарий для получения команды из хранилища.

        :return: TeamDTO, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            team_entity: Optional[TeamEntity] = await cls.repository.get_by_name(session, name)
            if team_entity:
                logger.info("Team found in repository")
            else:
                logger.info("Team not found in repository")
            return team_entity


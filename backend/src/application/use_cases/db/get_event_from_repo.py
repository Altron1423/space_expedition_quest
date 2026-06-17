import structlog

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from backend.src.application.dtos.event import EventDTO
from backend.src.application.mappers import EventMapper
from backend.src.infrastructures.repositories.event import EventRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import EventEntity

logger = structlog.get_logger(__name__)

class GetEventFromRepoUseCase:
    uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
    events_mapper: EventMapper = EventMapper()

    repository: EventRepositoriesSQLAlchemy = EventRepositoriesSQLAlchemy()

    @classmethod
    async def GetList(cls) -> list[EventDTO]:
        """
        Выполняет сценарий для всех задач из хранилища.

        :return: list[EventDTO], все найденные задачи.
        """

        async with cls.uow as session:
            event_entities: list[EventEntity] = await cls.repository.get_list(session)
            if len(event_entities) == 0:
                logger.info("Events not found in repository")
            else:
                logger.info("Events found in repository")
            return [
                cls.events_mapper.to_dto(event_entity)
                for event_entity in event_entities
            ]

    @classmethod
    async def GetById(cls, unique_id: UUID) -> Optional[EventEntity]:
        """
        Выполняет сценарий для получения задачи из хранилища.

        :return: EventEntity, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            event_entity: Optional[EventEntity] = await cls.repository.get_by_id(session, unique_id)
            if event_entity:
                logger.info("Event found in repository")
            else:
                logger.info("Event not found in repository")
            return event_entity

    @classmethod
    async def GetByName(cls, name: str) -> Optional[EventEntity]:
        """
        Выполняет сценарий для получения задачи из хранилища.

        :return: EventEntity, если она найдена в репозитории, в противном случае None.
        """

        async with cls.uow as session:
            event_entity: Optional[EventEntity] = await cls.repository.get_by_name(session, name)
            if event_entity:
                logger.info("Event found in repository")
            else:
                logger.info("Event not found in repository")
            return event_entity


from uuid import UUID

import structlog

from backend.src.application.dtos.event import EventDTO
from backend.src.application.exceptions import EventAlreadyExistsError
from backend.src.application.mappers import EventMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.repositories.event import EventRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy


logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
events_mapper: EventMapper = EventMapper()

repository: EventRepositoriesSQLAlchemy = EventRepositoriesSQLAlchemy()


async def SaveEventInRepoUseCase(dto: EventDTO) -> UUID:
    """
    Выполняет сценарий для сохранения команды в хранилище.

    :return: None
    """
    async with uow as session:
        event_entity = events_mapper.to_entity(
            dto=dto
        )

        try:
            await repository.save(
                session=session,
                event=event_entity,
            )
        except RepositoryConflictError as exc:
            raise EventAlreadyExistsError(
                f"Product '{event_entity.unique_id}' already exists"
            ) from exc
    return event_entity.unique_id

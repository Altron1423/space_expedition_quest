import structlog

from fastapi import HTTPException

from backend.src.application.dtos.event import EventDTO
from backend.src.application.use_cases.db.get_event_from_repo import (
    GetEventFromRepoUseCase,
)
from backend.src.infrastructures.exceptions import RepositoryGetError

logger = structlog.get_logger(__name__)


async def GetEventsUseCase() -> list[EventDTO]:
    """
    Выполняет возврата всех задач.

    :return: EventDTO, список всех найденных задач.
    """
    try:
        # Берёт из базы
        event_dto = await GetEventFromRepoUseCase.GetList()
        return event_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Event not found")



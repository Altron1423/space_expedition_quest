import structlog

from fastapi import HTTPException

from backend.src.application.exceptions import EventAlreadyExistsError
from backend.src.application.use_cases.db.create_event_in_repo import CreateEventInRepoUseCase
from backend.src.application.dtos.event import EventDTO, CreateEventDTO
from backend.src.application.use_cases.db.get_event_from_repo import (GetEventFromRepoUseCase)
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def CreateEventUseCase(dto: CreateEventDTO) -> EventDTO:
    """
    Создаёт новое соревнование и возвращает его.

    :return: EventDTO, созданная задача.
    """
    try:
        event_dto = await GetEventFromRepoUseCase.GetByName(dto.name)
        if event_dto is not None:
            raise EventAlreadyExistsError("Event with this name already exists")
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Events not found")

    try:
        unique_id = await CreateEventInRepoUseCase(dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Events not created")

    try:
        event_dto = await GetEventFromRepoUseCase.GetById(unique_id)
        if event_dto is None:
            raise RepositoryGetError()
        return event_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Events not found")

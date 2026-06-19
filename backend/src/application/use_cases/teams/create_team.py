import structlog

from fastapi import HTTPException

from application.use_cases.db.get_event_from_repo import GetEventFromRepoUseCase
from backend.src.application.exceptions import TeamAlreadyExistsError
from backend.src.application.use_cases.db.create_team_in_repo import CreateTeamInRepoUseCase
from backend.src.application.dtos.team import TeamDTO, CreateTeamDTO
from backend.src.application.use_cases.db.get_team_from_repo import (GetTeamFromRepoUseCase)
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def CreateTeamUseCase(dto: CreateTeamDTO) -> TeamDTO:
    """
    Создаёт новую задачу и возвращает её.

    :return: TeamDTO, созданная задача.
    """
    try:
        team_dto = await GetTeamFromRepoUseCase.GetByName(dto.name)
        if team_dto is not None:
            raise TeamAlreadyExistsError("Team with this name already exists")
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Teams check error")

    try:
        event_dto = await GetEventFromRepoUseCase.GetById(dto.event_id)
        if event_dto is None:
            raise TeamAlreadyExistsError("Event with this id not exists")
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Events not found")

    try:
        unique_id = await CreateTeamInRepoUseCase(dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Teams not created")

    try:
        team_dto = await GetTeamFromRepoUseCase.GetById(unique_id)
        if team_dto is None:
            raise RepositoryGetError()
        return team_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Teams not found")

import structlog

from fastapi import HTTPException

from backend.src.application.exceptions import TeamAlreadyExistsError
from backend.src.application.use_cases.db.create_team_in_repo import CreateTeamInRepoUseCase
from backend.src.application.dtos.team import TeamDTO, CreateTeamDTO
from backend.src.application.use_cases.db.get_team_from_repo import (
    GetTeamByIdFromRepoUseCase,
    GetTeamByNameFromRepoUseCase
)
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def CreateTeamUseCase(dto: CreateTeamDTO) -> TeamDTO:
    """
    Создаёт новую задачу и возвращает её.

    :return: TeamDTO, созданная задача.
    """
    try:
        problem_dto = await GetTeamByNameFromRepoUseCase(dto.name)
        if problem_dto is not None:
            raise TeamAlreadyExistsError("Team with this name already exists")
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Teams not found")

    try:
        unique_id = await CreateTeamInRepoUseCase(dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Teams not created")

    try:
        problem_dto = await GetTeamByIdFromRepoUseCase(unique_id)
        if problem_dto is None:
            raise RepositoryGetError()
        return problem_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Teams not found")

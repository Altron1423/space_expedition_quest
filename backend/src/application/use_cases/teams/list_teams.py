import structlog

from fastapi import HTTPException

from backend.src.application.dtos.team import TeamDTO
from backend.src.application.use_cases.db.get_team_from_repo import (
    GetTeamFromRepoUseCase,
)
from backend.src.infrastructures.exceptions import RepositoryGetError

logger = structlog.get_logger(__name__)


async def GetTeamsUseCase() -> list[TeamDTO]:
    """
    Выполняет возврата всех задач.

    :return: TeamDTO, список всех найденных задач.
    """
    try:
        # Берёт из базы
        team_dto = await GetTeamFromRepoUseCase.GetList()
        return team_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Team not found")



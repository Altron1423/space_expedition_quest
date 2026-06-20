from uuid import UUID

import structlog

from fastapi import HTTPException

from application.dtos.event import LeaderboardDTO
from application.dtos.team import TeamDTO
from application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from backend.src.infrastructures.exceptions import RepositoryGetError

logger = structlog.get_logger(__name__)


async def GetLeaderboardEventUseCase(event_id: UUID) -> list[LeaderboardDTO]:
    """
    Создаёт новое соревнование и возвращает его.

    :return: EventDTO, созданная задача.
    """
    try:
        teams_dto: list[TeamDTO] = await GetTeamFromRepoUseCase.GetByEventID(event_id)
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Events not found")

    passwords_dto = []
    for team_dto in teams_dto:
        passwords_dto.append(
            LeaderboardDTO(
                name=team_dto.name,
                score=0,
                stage=team_dto.stage_mow,
            )
        )

    return passwords_dto



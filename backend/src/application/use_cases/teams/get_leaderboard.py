from uuid import UUID

import structlog

from dataclasses import replace
from fastapi import HTTPException

from application.dtos.email import EmailDTO
from application.dtos.event import LeaderboardDTO
from application.dtos.password import PasswordDTO
from application.dtos.team import TeamPasswordDTO, TeamDTO
from application.security.password import password_generator, hashing
from application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from application.use_cases.db.save_team_in_repo import SaveTeamInRepoUseCase
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

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



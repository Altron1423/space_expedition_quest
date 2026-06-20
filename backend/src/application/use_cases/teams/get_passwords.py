from uuid import UUID

import structlog

from dataclasses import replace
from fastapi import HTTPException

from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from application.dtos.team import TeamPasswordDTO, TeamDTO
from application.security.password import password_generator, hashing
from application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from application.use_cases.db.save_team_in_repo import SaveTeamInRepoUseCase
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def GetPasswordUseCase(event_id: UUID) -> list[TeamPasswordDTO]:
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
        password = password_generator()
        passwords_dto.append(
            TeamPasswordDTO(
                name=team_dto.name,
                email=EmailDTO(value=team_dto.email.value),
                password=password,
            )
        )
        replace(team_dto, password=PasswordDTO(value=hashing(password)))
        try:
            await SaveTeamInRepoUseCase(team_dto)
        except RepositorySaveError as err:
            raise HTTPException(status_code=400, detail="Events not created")

    return passwords_dto



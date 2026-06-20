from datetime import datetime
from uuid import UUID
from random import randint

import structlog

from dataclasses import replace
from fastapi import HTTPException

from application.dtos.email import EmailDTO
from application.dtos.event import EventDTO
from application.dtos.password import PasswordDTO
from application.dtos.problem import ProblemDTO
from application.dtos.stage import StageDataDTO
from application.dtos.team import TeamPasswordDTO, TeamDTO
from application.security.password import password_generator, hashing
from application.use_cases.db.get_event_from_repo import GetEventFromRepoUseCase
from application.use_cases.db.get_problem_from_repo import GetProblemFromRepoUseCase
from application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from application.use_cases.db.save_team_in_repo import SaveTeamInRepoUseCase
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def StartStageUseCase(team_uuid: UUID) -> StageDataDTO:
    """
    Создаёт новое соревнование и возвращает его.

    :return: EventDTO, созданная задача.
    """
    try:
        team_dto: TeamDTO  | None = await GetTeamFromRepoUseCase.GetById(team_uuid)
        if team_dto is None:
            raise RepositoryGetError()
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Team not found")

    try:
        problems_dto: list[ProblemDTO] = await GetProblemFromRepoUseCase.GetByEvent_Stage(team_dto.event_id, team_dto.stage_mow)
        if problems_dto is None:
            raise RepositoryGetError()
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Team not found")

    n_problem = randint(0, len(problems_dto))
    problem = problems_dto[n_problem]
    n_data_set = randint(0, len(problem.data_sets))
    data_set = problem.data_sets[n_data_set]



    stage_data_dto = StageDataDTO(
        name=problem.name,
        text=problem.text.format(data_set.elements),
        stage=team_dto.stage_mow,
        png_name="this_is_pikcha_v_temu.png",
        problem_id=problem.unique_id,
        data_set_id=data_set.unique_id,
        max_time=problem.max_time,
        min_time=problem.min_time,
    )

    team_dto = replace(team_dto, start_stage=datetime.now())
    try:
        await SaveTeamInRepoUseCase(team_dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Events not created")

    return stage_data_dto



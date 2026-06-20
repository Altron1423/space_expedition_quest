from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4
from random import randint

import structlog

from dataclasses import replace
from fastapi import HTTPException

from application.dtos.problem import ProblemDTO
from application.dtos.stage import StageDataDTO, AnswerDataDTO, FinishStageDataDTO, StageDTO
from application.dtos.team import TeamDTO
from application.use_cases.db.get_problem_from_repo import GetProblemFromRepoUseCase
from application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from application.use_cases.db.save_team_in_repo import SaveTeamInRepoUseCase
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError

logger = structlog.get_logger(__name__)


async def FinishStageUseCase(team_uuid: UUID, answer_dto: AnswerDataDTO) -> FinishStageDataDTO:
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
        problem_dto: Optional[ProblemDTO] = await GetProblemFromRepoUseCase.GetById(answer_dto.problem_id)
        if problem_dto is None:
            raise RepositoryGetError()
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Team not found")


    for data_set in problem_dto.data_sets:
        if data_set.unique_id == answer_dto.data_set_id:
            break
    else:
        raise HTTPException(status_code=404, detail="Data set not found")

    if data_set.answer != answer_dto.answer:
        return FinishStageDataDTO(
        complete=False,
        comics_png_name=None
    )

    t = datetime.now(UTC)-team_dto.start_stage
    print(type(t), t)
    team_dto: TeamDTO = replace(
        team_dto,
        stages=team_dto.stages + [
            StageDTO(
                unique_id=uuid4(),
                team_id=team_dto.unique_id,
                stage=team_dto.stage_now,
                problem=problem_dto.unique_id,
                data_set=data_set.unique_id,
                answer=answer_dto.answer,
                duration=datetime.now(UTC)
            )
        ]
    )

    team_dto: TeamDTO = replace(
        team_dto,
        stage_now=team_dto.stage_now + 1
    )

    try:
        await SaveTeamInRepoUseCase(team_dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Events not created")


    return FinishStageDataDTO(
        complete=True,
        comics_png_name="this_is_comiks_v_temu.png"
    )

    # stage_data_dto = StageDataDTO(
    #     name=problem.name,
    #     text=problem.text.format(data_set.elements),
    #     stage=team_dto.stage_mow,
    #     png_name="this_is_pikcha_v_temu.png",
    #     problem_id=problem.unique_id,
    #     data_set_id=data_set.unique_id,
    #     max_time=problem.max_time,
    #     min_time=problem.min_time,
    # )
    #
    # team_dto = replace(team_dto, start_stage=datetime.now())
    # try:
    #     await SaveTeamInRepoUseCase(team_dto)
    # except RepositorySaveError as err:
    #     raise HTTPException(status_code=400, detail="Events not created")
    #
    # return stage_data_dto



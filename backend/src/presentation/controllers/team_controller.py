from uuid import UUID

from fastapi import APIRouter, Request, Body, Path

from application.dtos.email import EmailDTO
from application.dtos.stage import StageDataDTO, FinishStageDataDTO, AnswerDataDTO
from application.dtos.team import CreateTeamDTO
from application.use_cases.auth.token_validator import TokenValidatorUseCase, StatusEnum
from application.use_cases.teams.finish_stage import FinishStageUseCase
from application.use_cases.teams.get_passwords import GetPasswordUseCase
from application.use_cases.teams.start_stage import StartStageUseCase
from backend.src.application.use_cases.teams.list_teams import GetTeamsUseCase
from backend.src.application.use_cases.teams.create_team import CreateTeamUseCase
from backend.src.presentation.mappers.team import (
    TeamPresentationMapper,
    TeamsPresentationMapper, TeamsPasswordPresentationMapper, StageDataPresentationMapper,
    FinishStageDataPresentationMapper
)
from backend.src.presentation.schemas.request import (
    CreateTeamRequest, FinishStageRequest
)
from backend.src.presentation.schemas.responses import (
    TeamsResponseSchema,
    TeamResponseSchema, StageDataResponseSchema, FinishStageDataResponseSchema
)
from presentation.schemas.responses import ListTeamsPasswordResponseSchema

router = APIRouter(prefix="/team", tags=["Team"])

@router.get(
    "/get_all",
    response_model=TeamsResponseSchema,
    summary="Get all problems",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def get_teams(
    request: Request,
) -> TeamsResponseSchema:
    """
    Возвращает все существующие команды.
    :param request:
    :return:
    """

    await TokenValidatorUseCase(request, StatusEnum.admin)

    problems_dto = await GetTeamsUseCase()
    return TeamsPresentationMapper.to_response(problems_dto)


@router.post(
    "/register",
    response_model=TeamResponseSchema,
    summary="Create new problem",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def register_team(
    request: Request,
    body: CreateTeamRequest = Body(...),
) -> TeamResponseSchema:
    """
    Создание нового продукта.
    """

    await TokenValidatorUseCase(request)


    dto = CreateTeamDTO(
        name=body.name,
        email=EmailDTO(value=body.email),
        event_id=body.event_id,
    )
    team_dto = await CreateTeamUseCase(dto)
    return TeamPresentationMapper.to_response(team_dto)


@router.post(
    "/get_password_for_event/{event_id}",
    response_model=ListTeamsPasswordResponseSchema,
    summary="Create new problem",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def get_password_for_event(
    request: Request,
    event_id: UUID = Path(..., description="Product UUID")
) -> ListTeamsPasswordResponseSchema:
    """
    Получение паролей для команд.
    """

    await TokenValidatorUseCase(request, StatusEnum.admin)

    passwords_dto = await GetPasswordUseCase(event_id)

    return TeamsPasswordPresentationMapper.to_response(passwords_dto)


@router.get(
    "/start_stage",
    response_model=StageDataResponseSchema,
    summary="Start stage",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def start_stage(
    request: Request
) -> StageDataResponseSchema:
    """
    Получение неотсортированный массив с информацией о командах для отображения их списке лидеров.
    """

    team_uuid = await TokenValidatorUseCase(request, StatusEnum.team)

    stage_data_dto = await StartStageUseCase(team_uuid)



    return StageDataPresentationMapper.to_response(stage_data_dto)


@router.post(
    "/finish_stage",
    response_model=FinishStageDataResponseSchema,
    summary="Finished stage",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def finish_stage(
    request: Request,
    body: FinishStageRequest = Body(...)
) -> FinishStageDataResponseSchema:
    """
    Получение неотсортированный массив с информацией о командах для отображения их списке лидеров.
    """

    team_uuid = await TokenValidatorUseCase(request, StatusEnum.team)

    answer_dto = AnswerDataDTO(
        answer=body.answer,
        problem_id=body.problems_id,
        data_set_id=body.data_set_id
    )

    finish_stage_dto = await FinishStageUseCase(team_uuid, answer_dto)

    # finish_stage_dto = FinishStageDataDTO(
    #     complete=True,
    #     comics_png_name="this_is_comiks_v_temu.png"
    # )

    return FinishStageDataPresentationMapper.to_response(finish_stage_dto)


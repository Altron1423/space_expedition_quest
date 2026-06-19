from uuid import UUID

from fastapi import APIRouter, Request, Body, Path

from application.dtos.email import EmailDTO
from application.dtos.stage import StageDataDTO, FinishStageDataDTO
from application.dtos.team import CreateTeamDTO, TeamPasswordDTO
from application.use_cases.auth.token_validator import TokenValidatorUseCase, StatusEnum
# from backend.src.application.dtos.problem import CreateProblemDTO, DataSetDTO
# from backend.src.application.use_cases.auth.token_validator import TokenValidatorUseCase
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

    # await TokenValidatorUseCase(request, StatusEnum.admin)


    m = [
        TeamPasswordDTO(
            name="Team name 1",
            email="user@example.com",
            password="1234"
        )
    ]

    return TeamsPasswordPresentationMapper.to_response(m)


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

    await TokenValidatorUseCase(request, StatusEnum.team)

    m = StageDataDTO(
        name="This problem 1",
        text="Text problem 1",
        stage=1,
        png_name="this_is_pikcha_v_temu.png",
        problem_id="7932755b-b00c-4425-9c1d-91fc44947c5f",
        data_set_id="d2f1aad2-dc4a-487e-b8ae-05d339f3d5bb",
        max_time=480,
        min_time=180,
    )

    return StageDataPresentationMapper.to_response(m)


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

    await TokenValidatorUseCase(request, StatusEnum.team)

    m = FinishStageDataDTO(
        complete=True,
        comics_png_name="this_is_comiks_v_temu.png"
    )

    return FinishStageDataPresentationMapper.to_response(m)


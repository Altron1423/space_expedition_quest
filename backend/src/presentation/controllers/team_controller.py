from fastapi import APIRouter, Request, Body

from application.dtos.email import EmailDTO
from application.dtos.team import CreateTeamDTO
from application.use_cases.auth.token_validator import TokenValidatorUseCase, StatusEnum
# from backend.src.application.dtos.problem import CreateProblemDTO, DataSetDTO
# from backend.src.application.use_cases.auth.token_validator import TokenValidatorUseCase
from backend.src.application.use_cases.teams.list_teams import GetTeamsUseCase
from backend.src.application.use_cases.teams.create_team import CreateTeamUseCase
from backend.src.presentation.mappers.team import (
    TeamPresentationMapper,
    TeamsPresentationMapper
)
from backend.src.presentation.schemas.request import (
    CreateTeamRequest
)
from backend.src.presentation.schemas.responses import (
    TeamsResponseSchema,
    TeamResponseSchema
)


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
    "/create",
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
async def create_product(
    request: Request,
    body: CreateTeamRequest = Body(...),
) -> TeamResponseSchema:
    """
    Создание нового продукта.
    """

    await TokenValidatorUseCase(request, StatusEnum.admin)


    dto = CreateTeamDTO(
        name=body.name,
        email=EmailDTO(value=body.email),
        event_id=body.event_id,
    )

    product_dto = await CreateTeamUseCase(dto)
    return TeamPresentationMapper.to_response(product_dto)

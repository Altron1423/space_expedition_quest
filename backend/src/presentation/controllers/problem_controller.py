from uuid import UUID, uuid4

from fastapi import APIRouter, Request, Body

from application.use_cases.auth.token_validator import TokenValidatorUseCase
from backend.src.application.dtos.problem import CreateProblemDTO, DataSetDTO
# from backend.src.application.use_cases.auth.token_validator import TokenValidatorUseCase
from backend.src.application.use_cases.problems.list_problems import GetProblemsUseCase
from backend.src.application.use_cases.problems.create_problem import CreateProblemUseCase
from backend.src.presentation.mappers.problem import (
    ProblemsPresentationMapper,
    ProblemPresentationMapper
)
from backend.src.presentation.schemas.request import (
    CreateProblemRequest
)
from backend.src.presentation.schemas.responses import (
    ProblemsResponseSchema,
    ProblemResponseSchema
)


router = APIRouter(prefix="/problems", tags=["Problems"])

@router.get(
    "/get_all",
    response_model=ProblemsResponseSchema,
    summary="Get all problems",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def get_problems(
    request: Request,
) -> ProblemsResponseSchema:
    """
    Возвращает все существующие задачи.
    :param request:
    :return:
    """

    await TokenValidatorUseCase(request)

    problems_dto = await GetProblemsUseCase()
    return ProblemsPresentationMapper.to_response(problems_dto)


@router.post(
    "/create",
    response_model=ProblemResponseSchema,
    summary="Create new problem",
    responses={
        200: {"description": "Problems retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Problems not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def create_problem(
    request: Request,
    body: CreateProblemRequest = Body(...),
) -> ProblemResponseSchema:
    """
    Создание нового продукта.
    """

    await TokenValidatorUseCase(request)

    problem_uuid = uuid4()

    dto = CreateProblemDTO(
        unique_id=problem_uuid,
        name=body.name,
        text=body.text,
        data_sets=[
            DataSetDTO(
                unique_id=uuid4(),
                problem_id=problem_uuid,
                elements=dset.elements,
                answer=dset.answer,
            )
            for dset in body.data_set
        ],
    )

    product_dto = await CreateProblemUseCase(dto)
    return ProblemPresentationMapper.to_response(product_dto)




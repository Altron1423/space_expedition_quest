from uuid import UUID

from fastapi import APIRouter, Path, Request

from backend.src.application.use_cases.auth.token_validator import TokenValidatorUseCase
from backend.src.application.use_cases.process_example import ProcessExampleUseCase
from backend.src.presentation.mappers.example_mapper import ExamplePresentationMapper
from backend.src.presentation.schemas.responses import ExampleResponseSchema

router = APIRouter(prefix="/examples", tags=["Examples"])

@router.post(
    "/{unique_id}",
    response_model=ExampleResponseSchema,
    summary="Get example by unique id",
    responses={
        200: {"description": "Example retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Example not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def get_example(
    unique_id: UUID = Path(..., description="Example UUID"),
) -> ExampleResponseSchema:
    """
    Функция является примером для оформления кода.
    :param unique_id:
    :return:
    """

    example_dto = await ProcessExampleUseCase(str(unique_id))
    return ExamplePresentationMapper.to_response(example_dto)


@router.get(
    "/get_1",
    summary="return 1",
)
async def get_user_1(
    request: Request,
) -> int:
    """
    Тестовая команда, для проверки работы функции проверки валидности jwt токена.
    :param request:
    :return:
    """
    await TokenValidatorUseCase(request)
    return 1


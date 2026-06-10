from fastapi import APIRouter, Response, Request

from backend.src.application.use_cases.db.setup_database import SetupDatabaseUseCase

router = APIRouter(prefix="/db", tags=["DataBase"])

@router.post(
    "/setup_database",
    summary="Register a new user",
    responses={
        200: {"description": "Example retrieved successfully"}
    },
)
async def setup_database(
    request: Request
) -> dict[str, bool]:
    """
    Перезапись базы данных (будет ограниченна)
    :return:
    """

    await SetupDatabaseUseCase.SetupDatabase()
    return {'success': True}

    # example_dto = await RegisterUserUseCase(data, request, response)
    # return ExamplePresentationMapper.to_response(example_dto)

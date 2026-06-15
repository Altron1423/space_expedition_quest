from fastapi import APIRouter, Response, Request

from application.dtos.admin import CreateAdminDTO
from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from backend.src.application.use_cases.auth.login import AdminLoginUseCase, TeamLoginUseCase
from backend.src.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from backend.src.application.use_cases.auth.register import RegisterUseCase
from backend.src.presentation.mappers.auth import AuthPresentationMapper
from backend.src.presentation.schemas.request import AdminRegisterRequest, AdminLoginRequest, TeamLoginRequest
from backend.src.presentation.schemas.responses import TokenResponseSchema

router = APIRouter(prefix="/authorize", tags=["Authorize"])
router_admin = APIRouter(prefix="/admin")
router_team = APIRouter(prefix="/team")

@router_admin.post(
    "/register",
    response_model=TokenResponseSchema,
    summary="Register a new admin",
    responses={
        200: {"description": "Example retrieved successfully"}
    },
)
async def register_admin(
    body: AdminRegisterRequest,
    response: Response,
) -> TokenResponseSchema:
    """
    Выполняет процесс регистрации.

    :param body: Pydantic схема с согласием, почтой, паролем и именем.
    :param response: Доступ к ответу.

    :return: UserTokenResponseSchema, представляющий результатом выполнения, access token и refresh token.
    """



    tokens = await RegisterUseCase(body, response)

    return AuthPresentationMapper.tokens_to_response(tokens)

@router_admin.post(
    "/login",
    response_model=TokenResponseSchema,
    summary="Admin login",
    responses={
        200: {"description": "Example retrieved successfully"},
        401: {"description": "Incorrect or missing token)"}
    },
)
async def login_team(
    data: AdminLoginRequest,
    response: Response,
) -> TokenResponseSchema:
    """
    Выполняет процесс авторизации.

    :param data: Pydantic схема с почтой и паролем.
    :param response: Доступ к ответу.

    :return: UserTokenResponseSchema, представляющий результатом выполнения, access token и refresh token.
    """

    tokens = await AdminLoginUseCase(data, response)

    return AuthPresentationMapper.tokens_to_response(tokens)


@router_team.post(
    "/login",
    response_model=TokenResponseSchema,
    summary="Team login",
    responses={
        200: {"description": "Example retrieved successfully"},
        401: {"description": "Incorrect or missing token)"}
    },
)
async def login_admin(
    data: TeamLoginRequest,
    response: Response,
) -> TokenResponseSchema:
    """
    Выполняет процесс авторизации.

    :param data: Pydantic схема с почтой и паролем.
    :param response: Доступ к ответу.

    :return: UserTokenResponseSchema, представляющий результатом выполнения, access token и refresh token.
    """

    tokens = await TeamLoginUseCase(data, response)

    return AuthPresentationMapper.tokens_to_response(tokens)




@router.get(
    "/refresh",
    response_model=TokenResponseSchema,
    summary="User token refresh",
    responses={
        200: {"description": "Example retrieved successfully"},
        401: {"description": "Incorrect or missing token"}
    },
)
async def refresh_user(
    request: Request,
    response: Response,
) -> TokenResponseSchema:
    tokens = await RefreshTokenUseCase(request, response)
    return AuthPresentationMapper.tokens_to_response(tokens)



router.include_router(router_admin)
router.include_router(router_team)
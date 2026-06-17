import json

import structlog
from fastapi import HTTPException

from backend.src.application.exceptions import UserLoginError
from backend.src.application.security.password import is_correct
from backend.src.application.use_cases.auth.get_tocken import GetTokenUseCase
from backend.src.application.use_cases.db.get_team_from_repo import GetTeamFromRepoUseCase
from backend.src.application.use_cases.db.get_admin_from_repo import GetAdminFromRepoUseCase

from backend.src.infrastructures.exceptions import RepositoryGetError
from backend.src.presentation.schemas.request import AdminLoginRequest, TeamLoginRequest

logger = structlog.get_logger(__name__)


async def AdminLoginUseCase(data: AdminLoginRequest, response) -> dict[str, bool | str]:
    """
    Выполняет процесс авторизации администратора.

    :param data: Pydantic схема с почтой и паролем пользователя.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    try:
        # Берёт из базы
        if not (admin_entity := await GetAdminFromRepoUseCase.GetByEmail(data.email)):
            raise UserLoginError("Invalid email or password")
    except RepositoryGetError as err:
        raise HTTPException(status_code=520, detail="User unknow error")


    logger.info(
        "User login completed",
        unique_id=admin_entity.unique_id,
    )
    if is_correct(data.password.value, str(admin_entity.password)):
        tokens: dict[str, bool|str] = await GetTokenUseCase(json.dumps({'type': 'admin', 'unique_id': str(admin_entity.unique_id)}), response)
        return tokens

    raise UserLoginError("Invalid email or password")


async def TeamLoginUseCase(data: TeamLoginRequest, response) -> dict[str, bool | str]:
    """
    Выполняет процесс авторизации команды.

    :param data: Pydantic схема с почтой и паролем пользователя.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    try:
        # Берёт из базы
        if not (team_entity := await GetTeamFromRepoUseCase.GetByName(data.name)):
            raise UserLoginError("Invalid name or password")
    except RepositoryGetError as err:
        raise HTTPException(status_code=520, detail="User unknow error")


    logger.info(
        "User login completed",
        unique_id=team_entity.unique_id,
    )
    if is_correct(data.password.value, str(team_entity.password)):
        tokens: dict[str, bool|str] = await GetTokenUseCase(json.dumps({'type': 'team', 'unique_id': str(team_entity.unique_id)}), response)
        return tokens

    raise UserLoginError("Invalid name or password")

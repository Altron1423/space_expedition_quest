import uuid

import structlog
from fastapi import HTTPException

from backend.src.application.use_cases.auth.create_user import CreateUserUseCase
from backend.src.application.use_cases.auth.get_tocken import GetUserTokenUseCase
from backend.src.application.use_cases.db.get_user_from_repo import GetUserFromRepoUseCase

from backend.src.application.exceptions import UserNotAcceptTerms, EmailBeenUsedError

from backend.src.infrastructures.exceptions import RepositoryGetError

from backend.src.presentation.schemas.request import RegisterRequest

logger = structlog.get_logger(__name__)


async def RegisterUserUseCase(data: RegisterRequest, response) -> dict[str, bool|str]:
    """
    Выполняет процесс регистрации пользователя.

    :param data: Pydantic схема с почтой, паролем и подтверждением принятия правил пользования.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    if data.accept_terms == False:
        raise UserNotAcceptTerms("To register, you must accept the terms of use.")

    try:
        # Берёт из базы
        if await GetUserFromRepoUseCase.GetByEmail(data.email):
            raise EmailBeenUsedError("This mail is already busy. Use a different email address.")
    except RepositoryGetError as err:
        raise HTTPException(status_code=520, detail="User unknow error")

    user_entity = await CreateUserUseCase(data)
    tokens: dict[str, bool|str] = await GetUserTokenUseCase(user_entity.unique_id, response)

    logger.info(
        "User registration completed",
        unique_id=user_entity.unique_id,
    )

    return tokens


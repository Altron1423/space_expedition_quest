import structlog
from fastapi import HTTPException

from backend.src.application.exceptions import UserLoginError
from backend.src.application.security.password import is_correct
from backend.src.application.use_cases.auth.get_tocken import GetUserTokenUseCase
from backend.src.application.use_cases.db.get_user_from_repo import GetUserFromRepoUseCase

from backend.src.infrastructures.exceptions import RepositoryGetError
from backend.src.presentation.schemas.request import LoginRequest

logger = structlog.get_logger(__name__)


async def LoginUserUseCase(data: LoginRequest, response) -> dict[str, bool|str]:
    """
    Выполняет процесс авторизации пользователя.

    :param data: Pydantic схема с почтой и паролем пользователя.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    try:
        # Берёт из базы
        if not (user_entity := await GetUserFromRepoUseCase.GetByEmail(data.email)):
            raise UserLoginError("Invalid email or password")
    except RepositoryGetError as err:
        raise HTTPException(status_code=520, detail="User unknow error")


    logger.info(
        "User login completed",
        unique_id=user_entity.unique_id,
    )
    if is_correct(data.password.value, str(user_entity.password)):
        tokens: dict[str, bool|str] = await GetUserTokenUseCase(user_entity.unique_id, response)
        return tokens

    raise UserLoginError("Invalid email or password")


    return str(user_entity)


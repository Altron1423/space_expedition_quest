from uuid import UUID
import structlog
from fastapi import HTTPException

from backend.src.application.security.jwt_security import security
from backend.src.config.base import Settings

logger = structlog.get_logger(__name__)

settings: Settings = Settings()

async def GetTokenUseCase(data: str, response) -> dict[str, bool|str]:
    """
    Выполняет процесс создания jwt токенов доступа.

    :param unique_id: Информация, для сохранения в jwt.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    access_token = security.create_access_token(data)
    refresh_token = security.create_refresh_token(data)
    response.set_cookie(settings.jwt_access_cookie_name, access_token)
    response.set_cookie(settings.jwt_refresh_cookie_name, refresh_token)

    logger.debug(
        "Create tokens completed",
        data=data
    )

    return {"ok": True, "access_token": access_token, "refresh_token": refresh_token}

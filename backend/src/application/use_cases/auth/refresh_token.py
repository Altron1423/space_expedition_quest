from authx import exceptions
# import structlog

from backend.src.application.exceptions import MissingRefreshJWTTokenError, RefreshJWTDecodeError
from backend.src.application.security.jwt_security import security
from backend.src.application.use_cases.auth.get_tocken import GetTokenUseCase

# logger = structlog.get_logger(__name__)

async def RefreshTokenUseCase(request, response) -> dict[str, bool | str]:
    """
    Выполняет процесс обновления jwt токена доступа пользователя по refresh токену.

    :param request: Информация пользователя.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    try:
        refresh_payload = await security.refresh_token_required(request)
    except exceptions.MissingTokenError as e:
        raise MissingRefreshJWTTokenError(f"Undefined token in cookie.")
    except exceptions.JWTDecodeError as e:
        raise RefreshJWTDecodeError(f"Invalid token or the access token has expired.")

    tokens: dict[str, bool|str] = await GetTokenUseCase(refresh_payload.sub, response)
    return tokens


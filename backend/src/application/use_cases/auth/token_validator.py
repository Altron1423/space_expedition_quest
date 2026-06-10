from authx import exceptions
import structlog

from backend.src.application.exceptions import MissingAccessJWTTokenError, AccessJWTDecodeError
from backend.src.application.security.jwt_security import security
logger = structlog.get_logger(__name__)


async def TokenValidatorUseCase(request) -> str:
    """
    Выполняет процесс проверки наличия и валидности jwt токена доступа.

    :param request: Информация пользователя.

    :return: Информация сохранённая в jwt токене: UUID пользователя, которому он был выдан.
    """

    try:
        access_payload = await security.access_token_required(request)
    except exceptions.MissingTokenError as e:
        raise MissingAccessJWTTokenError(f"Undefined token in cookie")
    except exceptions.JWTDecodeError as e:
        raise AccessJWTDecodeError(f"Invalid token or the access token has expired.")

    return access_payload.sub


import json
import structlog
from fastapi import HTTPException

from application.dtos.admin import CreateAdminDTO
from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from application.use_cases.db.save_admin_in_repo import CreateAdminInRepoUseCase
from backend.src.application.security.password import hashing
from backend.src.application.use_cases.auth.get_tocken import GetTokenUseCase
from backend.src.application.use_cases.db.get_admin_from_repo import GetAdminFromRepoUseCase

from backend.src.application.exceptions import EmailBeenUsedError

from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError
from presentation.schemas.request import AdminRegisterRequest

logger = structlog.get_logger(__name__)


async def RegisterUseCase(body: AdminRegisterRequest, response) -> dict[str, bool | str]:
    """
    Выполняет процесс регистрации пользователя.

    :param body: Pydantic схема с почтой, паролем и подтверждением принятия правил пользования.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """

    dto = CreateAdminDTO(
        name=body.name,
        email=EmailDTO(value=body.email),
        password=PasswordDTO(value=hashing(body.password.value))
    )

    try:
        # Берёт из базы
        if await GetAdminFromRepoUseCase.GetByEmail(dto.email.value):
            raise EmailBeenUsedError("This mail is already busy. Use a different email address.")
    except RepositoryGetError as err:
        raise HTTPException(status_code=520, detail="User unknow error")

    try:
        admin_uuid = await CreateAdminInRepoUseCase(dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Teams not created")

    tokens: dict[str, bool|str] = await GetTokenUseCase(json.dumps({'type': 'admin', 'unique_id': str(admin_uuid)}), response)

    logger.info(
        "User registration completed",
        unique_id=admin_uuid,
    )

    return tokens


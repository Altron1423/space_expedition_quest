import structlog

from application.dtos.admin import CreateAdminDTO
from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from backend.src.application.security.password import hashing
from backend.src.application.use_cases.db.save_admin_in_repo import CreateAdminInRepoUseCase

from backend.src.domain.entities.admin import AdminEntity



from backend.src.presentation.schemas.request import AdminRegisterRequest

logger = structlog.get_logger(__name__)


async def CreateAdminUseCase(data: AdminRegisterRequest) -> AdminEntity:
    """
    Выполняет процесс создания пользователя и вызывает его сохранение.

    :param data: Pydantic схема с почтой, паролем и подтверждением принятия правил пользования.

    :return: АdminEntity, представляющий сущность пользователя.
    """

    admin_entity = CreateAdminDTO(
        name=data.name,
        email=EmailDTO(value=data.email),
        password=PasswordDTO(value=hashing(data.password.value)),
    )

    await CreateAdminInRepoUseCase(admin_entity)


    logger.debug(
        "Аdmin registration completed",
        unique_id=admin_entity.unique_id,
    )

    return admin_entity


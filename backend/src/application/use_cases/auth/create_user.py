from uuid import uuid1
import structlog


from backend.src.application.use_cases.db.save_cart_in_repo import SaveCartInRepoUseCase
from backend.src.application.use_cases.db.save_user_in_repo import SaveUserInRepoUseCase

from backend.src.application.security.password import hashing

from backend.src.domain.entities.user import UserEntity
from backend.src.domain.entities.cart import CartEntity
from backend.src.domain.value_objects.email_user import UserEmail
from backend.src.domain.value_objects.password import UserPassword



from backend.src.presentation.schemas.request import RegisterRequest

logger = structlog.get_logger(__name__)


async def CreateUserUseCase(data: RegisterRequest) -> UserEntity:
    """
    Выполняет процесс создания пользователя и вызывает его сохранение.

    :param data: Pydantic схема с почтой, паролем и подтверждением принятия правил пользования.

    :return: UserEntity, представляющий сущность пользователя.
    """

    cart_uuid = uuid1()
    user_entity = UserEntity(
        unique_id=uuid1(),
        username=data.username,
        password=UserPassword(hashing(data.password.value)),
        email=UserEmail(value=data.email),
        user_cart=cart_uuid
    )
    cart_entity = CartEntity(
        unique_id=cart_uuid,
        owner_id=user_entity.unique_id
    )

    await SaveCartInRepoUseCase.SaveCart(cart_entity)

    await SaveUserInRepoUseCase.SaveUser(user_entity)




    logger.debug(
        "User registration completed",
        unique_id=user_entity.unique_id,
    )

    return user_entity


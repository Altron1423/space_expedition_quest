from dataclasses import dataclass, field
from typing import final
from uuid import UUID

from backend.src.domain.exceptions import DomainValidationError
from domain.value_objects.email_user import UserEmail
from domain.value_objects.password import UserPassword


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AdminEntity:
    """
    Объект домена, представляющий собой задачу с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимые задачи не могут существовать.
    """
    unique_id: UUID
    name: str
    password: UserPassword = field(default_factory=UserPassword)
    email: UserEmail = field(default_factory=UserEmail)

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты AdminEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """

        if len(self.name) < 3 or len(self.name) > 20:
            raise DomainValidationError("Name must be between 3 and 20 characters.")


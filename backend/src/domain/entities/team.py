from dataclasses import dataclass, field
from typing import final
from uuid import UUID

from backend.src.domain.exceptions import DomainValidationError
from domain.entities.stage import StageEntity
from domain.value_objects.email_user import UserEmail
from domain.value_objects.password import UserPassword


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class TeamEntity:
    """
    Объект домена, представляющий собой задачу с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимые задачи не могут существовать.
    """
    unique_id: UUID
    name: str
    event_id: UUID
    password: UserPassword = field(default_factory=UserPassword)
    email: UserEmail = field(default_factory=UserEmail)
    stages: list[StageEntity]

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты TeamEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """

        if len(self.name) < 3 or len(self.name) > 20:
            raise DomainValidationError("Name must be between 3 and 20 characters.")


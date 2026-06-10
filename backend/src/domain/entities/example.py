from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import final
from uuid import UUID

from backend.src.domain.exceptions import DomainValidationError
from backend.src.domain.value_objects.example_size import ExampleSize


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExampleEntity:
    """
    Объект домена, представляющий собой example с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимый example не могут существовать.
    """
    unique_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    name: str
    size: ExampleSize = field(default_factory=ExampleSize)
    description: str | None = None

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты ExampleEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """

        if len(self.name) < 3 or len(self.name) > 20:
            raise DomainValidationError("Name must be between 3 and 20 characters.")


from dataclasses import dataclass
from typing import final
from uuid import UUID

from backend.src.domain.entities.data_set import DataSetEntity
from backend.src.domain.exceptions import DomainValidationError


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ProblemEntity:
    """
    Объект домена, представляющий собой задачу с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимые задачи не могут существовать.
    """
    unique_id: UUID
    name: str
    text: str
    stage: int
    data_sets: list[DataSetEntity]

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты ProblemEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """

        if len(self.name) < 3 or len(self.name) > 20:
            raise DomainValidationError("Name must be between 3 and 20 characters.")
        if len(self.text) == 0:
            raise DomainValidationError("The problem cannot be empty.")


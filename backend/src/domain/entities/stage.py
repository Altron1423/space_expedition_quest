from dataclasses import dataclass
from datetime import timedelta
from typing import final
from uuid import UUID

from backend.src.domain.entities.data_set import DataSetEntity
from backend.src.domain.entities.problem import ProblemEntity
# from backend.src.domain.exceptions import DomainValidationError


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StageEntity:
    """
    Объект домена, представляющий собой задачу с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимые задачи не могут существовать.
    """
    unique_id: UUID
    stage: int
    problem: ProblemEntity
    data_set: DataSetEntity
    answer: str
    duration: timedelta

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты StageEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """



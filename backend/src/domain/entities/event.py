from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID

from backend.src.domain.exceptions import DomainValidationError
from domain.entities.problem import ProblemEntity
from domain.entities.team import TeamEntity


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class EventEntity:
    """
    Объект домена, представляющий собой задачу с бизнес-инвариантами.
    Этот объект применяет бизнес-правила и поддерживает целостность данных
    на уровне домена, гарантируя, что недопустимые задачи не могут существовать.
    """
    unique_id: UUID
    name: str
    description: str
    location: str
    date: datetime
    teams: list[TeamEntity]
    problems: list[ProblemEntity]

    def __post_init__(self) -> None:
        """
        Проверяет бизнес-инварианты EventEntity.

        Объекты домена должны защищать свои инварианты и гарантировать,
        что недопустимое состояние не может существовать в модели домена.

        :return:
        :raise DomainValidationError: Если нарушен какой-либо бизнес-инвариант.
        """


from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID

from application.dtos.problem import ProblemDTO
from application.dtos.team import TeamDTO


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class EventDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (EventEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    name: str
    description: str
    location: str
    date: datetime
    teams: list[TeamDTO]
    problems: list[ProblemDTO]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateEventDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (EventEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    name: str
    description: str
    location: str
    date: datetime
    problems: list[UUID]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderboardDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (EventEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    name: str
    score: int
    stage: int

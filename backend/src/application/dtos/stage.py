from dataclasses import dataclass
from datetime import timedelta
from typing import final
from uuid import UUID

from application.dtos.problem import DataSetDTO, ProblemDTO


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StageDTO:

    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (StageEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    stage: int
    team_id: UUID
    problem: UUID
    data_set: UUID
    answer: str
    duration: timedelta


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class StageDataDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    name: str
    text: str
    stage: int
    png_name: str
    problem_id: UUID
    data_set_id: UUID
    max_time: int
    min_time: int


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class FinishStageDataDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    complete: bool
    comics_png_name: str | None


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AnswerDataDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    answer: str
    problem_id: UUID
    data_set_id: UUID

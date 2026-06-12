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
    problem: ProblemDTO
    data_set: DataSetDTO
    answer: str
    duration: timedelta

from dataclasses import dataclass
from typing import final
from uuid import UUID




@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DataSetDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (DatasetEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    problem_id: UUID
    elements: list[str]
    answer: str


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ProblemDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (ProblemEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    name: str
    text: str
    stage: int
    data_sets: list[DataSetDTO]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateProblemDTO:
    unique_id: UUID = None
    name: str
    text: str
    stage: int
    data_sets: list[DataSetDTO]


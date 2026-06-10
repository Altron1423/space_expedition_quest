from dataclasses import dataclass
from datetime import datetime
from typing import Literal, final
from uuid import UUID


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class SizeDTO:
    """Объект передачи данных для SizeDTO."""
    value: Literal[
        "big",
        "medium",
        "small"
    ]



@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExampleDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (ExampleEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    created_at: datetime
    name: str
    size: SizeDTO
    description: str | None = None



from dataclasses import dataclass
from typing import final
from uuid import UUID

from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from application.dtos.stage import StageDTO


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class TeamDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (TeamEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    name: str
    password: PasswordDTO
    email: EmailDTO
    stages: list[StageDTO]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTeamDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (TeamEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    name: str
    email: EmailDTO
    event_id: UUID



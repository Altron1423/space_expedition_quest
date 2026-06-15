from dataclasses import dataclass
from typing import final
from uuid import UUID

from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AdminDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (AdminEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    unique_id: UUID
    name: str
    password: PasswordDTO
    email: EmailDTO


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateAdminDTO:
    """Прикладной DTO для передачи данных примера между уровнями.

    Примечание: Этот DTO не выполняет бизнес-проверку.
    Бизнес-правила применяются сущностью домена (AdminEntity)…
    DTO являются простыми носителями данных для межуровневого взаимодействия.
    """

    name: str
    email: EmailDTO
    password: PasswordDTO



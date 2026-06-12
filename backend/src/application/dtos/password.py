from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordDTO:
    """Объект передачи данных для PasswordDTO."""
    value: str

    def __str__(self):
        return self.value

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class EmailDTO:
    """Объект передачи данных для EmailDTO."""
    value: str

    def __str__(self):
        return self.value

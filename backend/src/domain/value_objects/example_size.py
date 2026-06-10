from dataclasses import dataclass
from typing import ClassVar, final

from backend.src.domain.exceptions import InvalidSizeException


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExampleSize:
    """
    Объект Value, представляющий пример размера.
    Гарантирует, что значение материала является одним из предопределенных допустимых значений.
    """

    _allowed_values: ClassVar[set[str]] = {
        "big",
        "medium",
        "small"
    }

    value: str

    def __post_init__(self) -> None:
        """
        Проверяет значение размера после инициализации.
        Исключение:
            InvalidSizeException: Если указанное значение размера недопустимо.
        :return:
        """
        if self.value not in self._allowed_values:
            raise InvalidSizeException(f"Invalid size value: {self.value}")

    def __str__(self) -> str:
        """
        :return: Возвращает строковое представление размера.
        """
        return self.value

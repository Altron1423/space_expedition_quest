from dataclasses import dataclass
from typing import final

from backend.src.domain.exceptions import InvalidEmailException


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UserEmail:
    """
    Объект Value, представляющий пароль.
    Гарантирует, что значение материала является допустимых значений.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Проверяет значение почты после инициализации.
        Исключение:
            InvalidEmailException: Если указанное значение почты недопустимо.
        :return:
        """
        if self.value.find('@') == -1: # or self.value[self.value.find('@') + 1:] in ["yandex.ru", "gmail.com"]:
            """
            Для валидации почты достаточно получить символ '@', а после подтвердить через письмо (не реализовано по ТЗ).
            """
            raise InvalidEmailException(f"The email ({self.value}) must contain \'@\'.")

    def __str__(self) -> str:
        """
        :return: Возвращает строковое представление почты.
        """
        return self.value

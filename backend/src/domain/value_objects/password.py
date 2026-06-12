from dataclasses import dataclass

from backend.src.domain.exceptions import InvalidPasswordException

@dataclass(frozen=True)
class UserPassword:
    """
    Объект Value, представляющий пароль.
    Гарантирует, что значение материала является допустимых значений.
    """

    value: str

    def __post_init__(self):
        """
        Проверяет значение пароля после инициализации.
        Исключение:
            InvalidPasswordException: Если указанное значение пароля недопустимо.
        :return:
        """
        if len(self.value) == 0:
            raise InvalidPasswordException("Invalid password format")

    def __str__(self) -> str:
        """
        :return: Возвращает строковое представление пароля.
        """
        return self.value

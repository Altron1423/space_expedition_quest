from typing import final

@final
class PasswordError(Exception):
    """Исключение возникает при получении некорректного пароля."""
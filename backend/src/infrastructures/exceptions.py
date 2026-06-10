from typing import final

@final
class ExampleException(Exception):
    """Это образец исключения"""

class RepositorySaveError(Exception):
    """Исключение возникает при возникновении ошибки во время операции сохранения в репозитории."""

class RepositoryGetError(Exception):
    """Исключение возникает при возникновении ошибки во время операции получения данных в репозитории."""

class RepositoryConflictError(Exception):
    """Исключение возникает при возникновении конфликта во время работы репозитория."""
class RepositoryDeleteError(Exception):
    """Исключение возникает при возникновении конфликта во время работы репозитория."""
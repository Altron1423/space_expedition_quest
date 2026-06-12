from typing import final

@final
class ExampleNotFoundError(Exception):
    """Исключение возникает, когда example не найден."""

@final
class ProblemAlreadyExistsError(Exception):
    """Исключение возникает, когда задача уже существует"""

@final
class CreateProblemUuidIsNone(Exception):
    """Исключение возникает, если в dto не был присвоен uuid"""

# @final
# class ProductNotFoundError(Exception):
#     """Исключение возникает, когда product не найден"""
#
# @final
# class PermissionDeniedError(Exception):
#     """Исключение возникает, когда у пользователя недостаточно прав"""
#
# @final
# class ProductPermissionDeniedError(Exception):
#     """Исключение возникает, когда у пользователя недостаточно прав для обращения к product"""
#
# @final
# class PaginationValidationError(Exception):
#     """Некорректные параметры пагинации."""
#
@final
class UserNotAcceptTerms(Exception):
    """Исключение возникает, когда пользователь не принял правила пользования."""

@final
class EmailBeenUsedError(Exception):
    """Исключение возникает при попытке создать нового пользователя по ранее использованной почте."""

@final
class UserLoginError(Exception):
    """Исключение возникает, когда пользователь не найден."""

@final
class MissingAccessJWTTokenError(Exception):
    """Исключение возникает при отсутствии JWT токена."""

@final
class MissingRefreshJWTTokenError(Exception):
    """Исключение возникает при отсутствии JWT токена."""

@final
class AccessJWTDecodeError(Exception):
    """Исключение возникает при некорректном JWT или истечении его времени действия."""

@final
class RefreshJWTDecodeError(Exception):
    """Исключение возникает при некорректном JWT или истечении его времени действия."""

# @final
# class UndefinedUserCartError(Exception):
#     """Возникает, если корзина пользователя была не найдена"""
#
# @final
# class ProductInCart(Exception):
#     """Возникает, если нахождение продукт в корзине не соответствует ожидаемости"""

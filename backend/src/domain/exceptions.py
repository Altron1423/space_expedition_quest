from typing import final


@final
class DomainValidationError(Exception):
    """Вызывается при сбое проверки валидности."""

@final
class InvalidSizeException(Exception):
    """Возникает при сбое проверки объекта example_size."""

@final
class InvalidPasswordException(Exception):
    """Возникает при сбое проверки объекта UserPassword."""

@final
class InvalidEmailException(Exception):
    """Возникает при сбое проверки объекта UserEmail."""

@final
class InvalidProductTitleException(Exception):
    """Возникает при сбое проверки объекта ProductTitle."""

@final
class InvalidProductDescriptionException(Exception):
    """Возникает при сбое проверки объекта ProductDescription."""

@final
class InvalidProductPriceException(Exception):
    """Возникает при сбое проверки объекта ProductPrice. """

@final
class InvalidCategoryNameException(Exception):
    """Возникает при сбое проверки объекта CategoryName."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.src.domain.exceptions import (
    DomainValidationError,
    InvalidSizeException,
    InvalidEmailException,
    InvalidPasswordException, InvalidProductTitleException, InvalidProductDescriptionException,
    InvalidProductPriceException, InvalidCategoryNameException
)

from backend.src.application.exceptions import (
    ExampleNotFoundError,
    UserNotAcceptTerms,
    EmailBeenUsedError,
    UserLoginError,
    MissingAccessJWTTokenError,
    AccessJWTDecodeError,
    MissingRefreshJWTTokenError,
    RefreshJWTDecodeError,
)

from backend.src.infrastructures.exceptions import (
    RepositorySaveError,
    RepositoryGetError,
    RepositoryConflictError, RepositoryDeleteError
)

from backend.src.presentation.exceptions import (
    PasswordError
)



def setup_exception_handlers(app: FastAPI) -> None:
    """
    Добавленные сюда исключения не будут срабатывать как ошибка и вылетать в консоль.
    Вместо этого они отправятся клиенту в описанном тут формате, можно настроить код и оформление исключения.
    exc - сообщение переданное в исключение при вызове в коде.

    :param app: Экземпляр приложения FastAPI, для которого необходимо добавить исключения
    :return:
    """

    """
        Исключения домена
    """
    @app.exception_handler(DomainValidationError)
    async def domain_validation_error_handler(
        request: Request,
        exc: DomainValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidSizeException)
    async def invalid_size_exception_handler(
        request: Request,
        exc: InvalidSizeException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidEmailException)
    async def invalid_email_exception_handler(
        request: Request,
        exc: InvalidEmailException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_exception_handler(
        request: Request,
        exc: InvalidPasswordException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidProductTitleException)
    async def invalid_product_title_exception_handler(
            request: Request,
            exc: InvalidProductTitleException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidProductDescriptionException)
    async def invalid_product_description_exception_handler(
            request: Request,
            exc: InvalidProductDescriptionException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidProductPriceException)
    async def invalid_product_price_exception_handler(
            request: Request,
            exc: InvalidProductPriceException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidCategoryNameException)
    async def invalid_product_price_exception_handler(
            request: Request,
            exc: InvalidCategoryNameException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )


    """
        Исключения приложения
    """
    @app.exception_handler(ExampleNotFoundError)
    async def example_not_found_exception_handler(
        request: Request,
        exc: ExampleNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserNotAcceptTerms)
    async def user_not_accept_terms_exception_handler(
        request: Request,
        exc: UserNotAcceptTerms,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(EmailBeenUsedError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: EmailBeenUsedError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserLoginError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: UserLoginError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(MissingAccessJWTTokenError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: MissingAccessJWTTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(MissingRefreshJWTTokenError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: MissingRefreshJWTTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(AccessJWTDecodeError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: AccessJWTDecodeError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(RefreshJWTDecodeError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: RefreshJWTDecodeError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    """
        Исключения инфраструктуры
    """
    @app.exception_handler(RepositorySaveError)
    async def example_not_found_exception_handler(
        request: Request,
        exc: RepositorySaveError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(RepositoryGetError)
    async def user_not_accept_terms_exception_handler(
        request: Request,
        exc: RepositoryGetError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(RepositoryConflictError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: RepositoryConflictError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(RepositoryDeleteError)
    async def repository_delete_exception_handler(
            request: Request,
            exc: RepositoryDeleteError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )


    """
        Исключения демонстрации
    """
    @app.exception_handler(PasswordError)
    async def example_not_found_exception_handler(
        request: Request,
        exc: PasswordError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )


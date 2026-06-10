from typing import Literal
from collections.abc import Sequence

from pydantic import Field
from pydantic_settings import BaseSettings

from backend.src.config.app import AppSettings
from backend.src.config.database import DatabaseSettings
from backend.src.config.jwt_auth import JWTSettings


class Settings(BaseSettings):
    """
    Основные настройки приложения, объединяющие все объекты конфигурации.

    Этот класс служит в качестве фасада, который обеспечивает доступ ко всем
    разделам конфигурации приложения. Каждый раздел конфигурации несет ответственность за
    определенного домена (базы данных, redis, cors и т.д.).
    """

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)

    # Convenience properties for backward compatibility
    @property
    def app_name(self) -> str:
        """Get application name."""
        return self.app.app_name

    @property
    def environment(self) -> str:
        """Get application environment."""
        return self.app.environment

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.app.log_level

    @property
    def debug(self) -> bool:
        """Get debug flag."""
        return self.app.debug

    @property
    def database_url(self) -> str:
        """Get database URL."""
        return str(self.database.database_url)

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Get SQLAlchemy database URI."""
        return str(self.database.sqlalchemy_database_uri)

    @property
    def postgres_user(self) -> str:
        """Get PostgreSQL username."""
        return self.database.postgres_user

    @property
    def postgres_password(self) -> str:
        """Get PostgreSQL password."""
        return self.database.postgres_password

    @property
    def postgres_server(self) -> str:
        """Get PostgreSQL server."""
        return self.database.postgres_host

    @property
    def postgres_port(self) -> int:
        """Get PostgreSQL port."""
        return self.database.postgres_port

    @property
    def postgres_db(self) -> str:
        """Get PostgreSQL database name."""
        return self.database.postgres_db

    @property
    def jwt_secret_key(self) -> str:
        """Get JWT secret key."""
        return self.jwt.jwt_secret_key

    @property
    def jwt_access_cookie_name(self) -> str:
        """Get JWT access cookie name."""
        return self.jwt.jwt_access_cookie_name

    @property
    def jwt_refresh_cookie_name(self) -> str:
        """Get JWT refresh cookie name."""
        return self.jwt.jwt_refresh_cookie_name

    @property
    def jwt_cookie_csrf_protect(self) -> bool:
        """Get JWT cookie CSRF protect."""
        return self.jwt.jwt_cookie_csrf_protect

    @property
    def jwt_token_location(self) -> Sequence[Literal[
        "headers", "cookies", "json", "query"
    ]]:
        """Get JWT token location."""
        return self.jwt.jwt_token_location

    @property
    def jwt_algorithm(self) -> Literal[
        "HS256",
        "HS384",
        "HS512",
        "ES256",
        "ES256K",
        "ES384",
        "ES512",
        "RS256",
        "RS384",
        "RS512",
        "PS256",
        "PS384",
        "PS512"
    ]:
        """Get JWT algorithm."""
        return self.jwt.jwt_algorithm

    @property
    def hash_algorithm(self) -> str:
        """Get hash algorithm."""
        return self.jwt.hash_algorithm

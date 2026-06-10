from typing import cast, final

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings


@final
class DatabaseSettings(BaseSettings):
    """
    Параметры конфигурации базы данных.

    Attributes:
        postgres_user (str): имя пользователя PostgreSQL.
        postgres_password (str): пароль PostgreSQL.
        postgres_host (str): хост сервера PostgreSQL.
        postgres_port (int): порт сервера PostgreSQL.
        postgres_db (str): имя базы данных PostgreSQL.
    """

    use_postgres: bool = Field(False, alias="USE_POSTGRESQL")

    url_local_bd: str = Field(..., alias="URL_LOCAL_BD")

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(..., alias="POSTGRES_HOST")
    postgres_port: int = Field(..., alias="POSTGRES_PORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    @computed_field
    def database_url(self) -> str | PostgresDsn:
        if self.use_postgres:
            return self.database_url_Postgres
        else:
            return self.database_url_local


    @computed_field
    def database_url_local(self) -> str:
        """
        :return str: ссылка на файл локальной базы данных.
        """
        return f"sqlite+aiosqlite:///{self.url_local_bd}"

    @computed_field
    def database_url_Postgres(self) -> PostgresDsn:
        """
        Создает URL-адрес базы данных PostgreSQL.

        :return PostgresDsn: URL-адрес созданной базы данных.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        """
        Returns the SQLAlchemy compatible database URI.

        :return PostgresDsn: The SQLAlchemy database URI.
        """
        return cast("PostgresDsn", self.database_url)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

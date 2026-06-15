from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base


class AdminModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "admin" в базе данных.
    """

    __tablename__ = 'admin'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(length=20), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=False)



    def __repr__(self) -> str:
        """
        :return: строковое представление AdminModel.
        """
        return (
            f'<AdminModel(id={self.unique_id}> name={self.name})>'
        )



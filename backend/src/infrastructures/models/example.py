from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base



class ExampleModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "example" в базе данных.
    """

    __tablename__ = 'example'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now()
    )

    name: Mapped[str] = mapped_column(String(length=20), nullable=False)
    size: Mapped[str] = mapped_column(String(length=10), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        """
        :return: строковое представление ExampleModel.
        """
        return (
            f'<ExampleModel(id={self.unique_id}> '
            f'name={self.name}, size={self.size})>'
        )



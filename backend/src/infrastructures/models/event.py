from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base


class EventModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "event" в базе данных.
    """

    __tablename__ = 'event'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(length=20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now()
    )

    teams: Mapped[list["TeamModel"]] = relationship(
        back_populates="events",
        secondary="team_event_bind",
        lazy="selectin"
    )

    problems: Mapped[list["ProblemModel"]] = relationship(
        back_populates="events",
        secondary="problem_event_bind",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        """
        :return: строковое представление EventModel.
        """
        return (
            f'<EventModel(id={self.unique_id}> name={self.name})>'
        )



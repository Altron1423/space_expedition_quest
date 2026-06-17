from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base


class TeamModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "team" в базе данных.
    """

    __tablename__ = 'team'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(length=20), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=False)

    event_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("event.unique_id"),
        nullable=False,
    )

    stages: Mapped[list["StageModel"]] = relationship(
        "StageModel",
        back_populates="team"
    )
    events: Mapped["EventModel"] = relationship(
        back_populates="teams",
        secondary="team_event_bind"
    )



    def __repr__(self) -> str:
        """
        :return: строковое представление TeamModel.
        """
        return (
            f'<TeamModel(id={self.unique_id}> name={self.name})>'
        )



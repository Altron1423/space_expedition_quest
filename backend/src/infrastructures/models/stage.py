from datetime import timedelta
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base
from backend.src.infrastructures.models.team import TeamModel


class StageModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "stage" в базе данных.
    """

    __tablename__ = 'stage'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    stage: Mapped[int] = mapped_column(
        nullable=False,
    )

    team_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("team.unique_id"),
        nullable=False
    )
    problem: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("problem.unique_id"),
        nullable=False,
    )
    data_set: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("data_set.unique_id"),
        nullable=False,
    )

    team: Mapped[TeamModel] = relationship(
        "TeamModel",
        back_populates="stages",
        cascade='save-update, merge'
    )

    answer: Mapped[str] = mapped_column(nullable=False)

    duration: Mapped[timedelta] = mapped_column(DateTime(timezone=True))


    def __repr__(self) -> str:
        """
        :return: строковое представление StageModel.
        """
        return (
            f'<StageModel(id={self.unique_id}> name={self.name})>'
        )



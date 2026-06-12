from datetime import timedelta
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base


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
    stage: Mapped[int]

    team_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("team.unique_id"),
        nullable=False,
    )
    problem_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("problem.unique_id"),
        nullable=False,
    )
    data_set_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("data_set.unique_id"),
        nullable=False,
    )

    team: Mapped["TeamModel"] = relationship(
        "TeamModel",
        back_populates="stages"
    )
    problem: Mapped["ProblemModel"] = relationship(
        "ProblemModel",
        back_populates="stages"
    )
    data_set: Mapped["DataSetModel"] = relationship(
        "DataSetModel",
        back_populates="stages"
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



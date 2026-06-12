from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base
from backend.src.infrastructures.models.data_set import DataSetModel


class ProblemModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "problem" в базе данных.
    """

    __tablename__ = 'problem'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(length=20), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    data_sets: Mapped[list[DataSetModel]] = relationship(
        "DataSetModel",
        back_populates="problem"
    )
    stages: Mapped[list["StageModel"]] = relationship(
        "StageModel",
        back_populates="problem"
    )

    def __repr__(self) -> str:
        """
        :return: строковое представление ProblemModel.
        """
        return (
            f'<ProblemModel(id={self.unique_id}> name={self.name})>'
        )



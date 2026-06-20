from uuid import UUID


from sqlalchemy import ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from backend.src.infrastructures.models.base import Base



class DataSetModel(Base):
    """
    Модель SQLAlchemy для хранения примеров данных.

    Сопоставляется с таблицей "data_set" в базе данных.
    """

    __tablename__ = 'data_set'

    unique_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    element:  Mapped[list[str]] = mapped_column(JSON)
    answer: Mapped[str] = mapped_column(Text, nullable=False)


    problem_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("problem.unique_id"),
        nullable=False,
    )

    problem: Mapped["ProblemModel"] = relationship(
        "ProblemModel",
        back_populates="data_sets",
        cascade='save-update, merge'
    )


    def __repr__(self) -> str:
        """
        :return: строковое представление DataSetModel.
        """
        return (
            f'<DataSetModel(id={self.unique_id}> problem={self.problem_id})>'
        )



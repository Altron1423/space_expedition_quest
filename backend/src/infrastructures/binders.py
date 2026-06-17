from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.infrastructures.models.base import Base


class TeamEventBinder(Base):
    __tablename__ = 'team_event_bind'
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4
    )
    team_id: Mapped[UUID] = mapped_column(
        ForeignKey("team.unique_id", ondelete="CASCADE")
    )
    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("event.unique_id", ondelete="CASCADE")
    )

class ProblemEventBinder(Base):
    __tablename__ = 'problem_event_bind'
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4
    )
    problem_id: Mapped[UUID] = mapped_column(
        ForeignKey("problem.unique_id", ondelete="CASCADE")
    )
    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("event.unique_id", ondelete="CASCADE")
    )
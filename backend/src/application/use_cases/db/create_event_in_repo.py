from uuid import UUID, uuid4

import structlog

from application.use_cases.db.get_problem_from_repo import GetProblemFromRepoUseCase
from backend.src.application.dtos.event import CreateEventDTO
from backend.src.application.exceptions import EventAlreadyExistsError
from backend.src.application.mappers import CreateEventMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.repositories.event import EventRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy
from domain.entities.event import EventEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
events_mapper: CreateEventMapper = CreateEventMapper()

repository: EventRepositoriesSQLAlchemy = EventRepositoriesSQLAlchemy()


async def CreateEventInRepoUseCase(dto: CreateEventDTO) -> UUID:
    """
    Выполняет сценарий для создания команды в хранилище.

    :return: None
    """

    problems_entity = []
    for problem_uuid in dto.problems:
        problem = await GetProblemFromRepoUseCase.GetById(problem_uuid)
        if problem is not None:
            problems_entity.append(problem)

    async with uow as session:
        event_entity = EventEntity(
            unique_id=uuid4(),
            name=dto.name,
            description=dto.description,
            location=dto.location,
            date=dto.date,
            teams=[],
            problems=problems_entity
        )


        try:
            await repository.save(
                session=session,
                event=event_entity,
            )
        except RepositoryConflictError as exc:
            raise EventAlreadyExistsError(
                f"Product '{event_entity.unique_id}' already exists"
            ) from exc
    return event_entity.unique_id

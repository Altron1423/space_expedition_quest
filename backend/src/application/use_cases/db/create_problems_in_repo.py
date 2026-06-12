import structlog

from typing import TYPE_CHECKING
from uuid import uuid4

from backend.src.application.dtos.problem import CreateProblemDTO
from backend.src.application.exceptions import ProblemAlreadyExistsError
from backend.src.application.mappers import CreateProblemMapper
from backend.src.infrastructures.exceptions import RepositoryConflictError
from backend.src.infrastructures.mappers.problem import ProblemDBMapper
from backend.src.infrastructures.repositories.problem import ProblemRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import ProblemEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
problems_mapper: CreateProblemMapper = CreateProblemMapper()

repository: ProblemRepositoriesSQLAlchemy = ProblemRepositoriesSQLAlchemy()


async def CreateProblemInRepoUseCase(dto: CreateProblemDTO) -> None:
    """
    Выполняет сценарий для создания задачи в хранилище.

    :return: None
    """
    unique_id = uuid4()
    async with uow as session:

        problem_entity = problems_mapper.to_entity(
            dto=dto
        )

        try:
            await repository.save(
                session=session,
                problem=problem_entity,
            )
        except RepositoryConflictError as exc:
            raise ProblemAlreadyExistsError(
                f"Product '{unique_id}' already exists"
            ) from exc


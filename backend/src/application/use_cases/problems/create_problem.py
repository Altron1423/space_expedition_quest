import structlog
from fastapi import HTTPException

from backend.src.application.dtos.problem import ProblemDTO, CreateProblemDTO
from backend.src.application.use_cases.db.create_problems_in_repo import CreateProblemInRepoUseCase
from backend.src.application.use_cases.db.get_problem_from_repo import GetProblemByIdFromRepoUseCase
from backend.src.infrastructures.exceptions import RepositorySaveError
from backend.src.infrastructures.exceptions import RepositoryGetError

logger = structlog.get_logger(__name__)


async def CreateProblemUseCase(dto: CreateProblemDTO) -> ProblemDTO:
    """
    Создаёт новую задачу и возвращает её.

    :return: ProblemDTO, созданная задача.
    """
    try:
        await CreateProblemInRepoUseCase(dto)
    except RepositorySaveError as err:
        raise HTTPException(status_code=400, detail="Problems not created")

    try:
        problem_dto = await GetProblemByIdFromRepoUseCase(dto.unique_id)
        if problem_dto is None:
            raise RepositoryGetError()
        return problem_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Problems not found")

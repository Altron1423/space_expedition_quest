import structlog

from fastapi import HTTPException

from backend.src.application.dtos.problem import ProblemDTO
from backend.src.application.use_cases.db.get_problem_from_repo import (
    GetProblemFromRepoUseCase,
)
from backend.src.infrastructures.exceptions import RepositoryGetError

logger = structlog.get_logger(__name__)


async def GetProblemsUseCase() -> list[ProblemDTO]:
    """
    Выполняет возврата всех задач.


    :return: ProblemDTO, список всех найденных задач.
    """
    try:
        # Берёт из базы
        problem_dto = await GetProblemFromRepoUseCase.GetLis()
        return problem_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Problems not found")

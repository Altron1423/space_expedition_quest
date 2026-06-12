from uuid import UUID

import structlog
from fastapi import HTTPException

from backend.src.application.dtos.problem import ProblemDTO, DataSetDTO
from backend.src.application.use_cases.db.get_problem_from_repo import (
    GetProblemsListFromRepoUseCase,
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
        problem_dto = await GetProblemsListFromRepoUseCase()
        return problem_dto
    except RepositoryGetError as err:
        raise HTTPException(status_code=404, detail="Problems not found")

    problem_dto = ProblemDTO(
        unique_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        name="errr",
        text="THIS SHOULD NOT BE USED {}",
        data_set=[
            DataSetDTO(
                unique_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66ffa6"),
                problem=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                elements=["error"],
                answer="ERROR"
            )
        ]
    )

    logger.info(
        "Example successfully fetched and processed",
    )
    return [problem_dto]


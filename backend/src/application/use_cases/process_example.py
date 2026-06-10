from datetime import datetime
from typing import TYPE_CHECKING

import structlog
from fastapi import HTTPException

from backend.src.application.dtos.example import ExampleDTO, SizeDTO
from backend.src.application.use_cases.db.get_example_from_repo import (
    GetExampleFromRepoUseCase,
)
from backend.src.infrastructures.exceptions import RepositorySaveError

if TYPE_CHECKING:
    pass

logger = structlog.get_logger(__name__)


async def ProcessExampleUseCase(unique_id: str) -> ExampleDTO | None:
    """
    Выполняет процесс обработки example.

    :param unique_id: Идентификатор обрабатываемого example.

    :return: ExampleDTO, представляющий обработанный артефакт.
    """
    try:
        # Берёт из базы
        if example_dto := await GetExampleFromRepoUseCase(unique_id):
            return example_dto
    except RepositorySaveError as err:
        raise HTTPException(status_code=404, detail="Example not found")

    example_dto = ExampleDTO(
        unique_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        created_at=datetime.now(),
        name="qq",
        size=SizeDTO(value="big"),
        description="THIS SHOULD NOT BE USED",
    )

    logger.info(
        "Example successfully fetched and processed",
        unique_id=unique_id,
    )
    return example_dto


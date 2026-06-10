from typing import TYPE_CHECKING

import structlog

from backend.src.application.dtos.example import ExampleDTO
from backend.src.application.mappers import ExampleMapper
from backend.src.infrastructures.repositories.example import ExampleRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

if TYPE_CHECKING:
    from backend.src.domain.entities.example import ExampleEntity

logger = structlog.get_logger(__name__)


uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()
example_mapper: ExampleMapper = ExampleMapper()

repository: ExampleRepositoriesSQLAlchemy = ExampleRepositoriesSQLAlchemy


async def GetExampleFromRepoUseCase(unique_id: str) -> ExampleDTO | None:
    """
    Выполняет сценарий для получения example из хранилища.

    :param unique_id: Идентификатор извлекаемого example.

    :return: ExampleDTO, если он найден в репозитории, в противном случае отсутствует.
    """

    async with uow as session:
        example_entity: (
            ExampleEntity | None
        ) = await repository.get_by_id(session, unique_id)
        if example_entity:
            logger.info("Example found in repository", inventory_id=unique_id)
            return example_mapper.to_dto(example_entity)
        logger.info("Example not found in repository", inventory_id=unique_id)
        return None


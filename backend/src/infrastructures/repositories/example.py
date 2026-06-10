from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.domain.entities.example import ExampleEntity
from backend.src.infrastructures.exceptions import RepositorySaveError, RepositoryConflictError
from backend.src.infrastructures.mappers.example import ExampleDBMapper
from backend.src.infrastructures.models.example import ExampleModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExampleRepositoriesSQLAlchemy:
    """
    Реализация репозитория example на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    Логика сопоставления делегирована ExampleDBMapper в соответствии с SRP.
    """

    mapper: ExampleDBMapper

    @classmethod
    async def get_by_id(
            cls,
            session: AsyncSession,
            example_id: str | UUID
    ) -> ExampleEntity | None:
        """
        Извлекает артефакт из базы данных по его инвентарному идентификатору.

        :param example_id: Уникальный идентификатор артефакта.
        :return: Артефакт, если он найден, в противном случае - нет.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(ExampleModel).where(
                ExampleModel.unique_id == example_id
            )
            result = await session.execute(stmt)
            example_model = result.scalar_one_or_none()
            if example_model is None:
                return None
            return cls.mapper.to_entity(example_model)
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to retrieve example by example_id '{example_id}': {err}"
            ) from err

    @classmethod
    async def save(
            cls,
            session: AsyncSession,
            example: ExampleEntity
    ) -> None:
        """
        Сохраняет новый артефакт или обновляет существующий в базе данных.

        :param example: ExampleEntity, которое должно сохраняться.
        :return:
        :raise RepositoryConflictError: Если во время сохранения нарушено уникальное ограничение.
        :raise RepositorySaveError: Если во время сохранения возникает ошибка базы данных.
        """
        try:
            stmt = select(ExampleModel).where(
                ExampleModel.unique_id == example.unique_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Обновите существующую модель с помощью mapper
                cls.mapper.update_model_from_entity(model, example)
            else:
                # Создание новой модели с помощью mapper
                model = cls.mapper.to_model(example)

            session.add(model)
        except IntegrityError as err:
            raise RepositoryConflictError(
                f"Conflict while saving example '{example.unique_id}': {err}"
            ) from err
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to save example '{example.unique_id}': {err}"
            ) from err
        except Exception as err:
            raise RepositorySaveError(
                f"Unexpected error while saving example '{example.unique_id}': {err}"
            ) from err

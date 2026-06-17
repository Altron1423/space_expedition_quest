from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.event import EventEntity
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError, RepositoryConflictError
from backend.src.infrastructures.mappers.event import EventDBMapper
from backend.src.infrastructures.models.event import EventModel


@dataclass(frozen=True, slots=True, kw_only=True)
class EventRepositoriesSQLAlchemy:
    """
    Реализация репозитория event на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    Логика сопоставления делегирована EventDBMapper в соответствии с SRP.
    """

    mapper: EventDBMapper = EventDBMapper

    async def get_list(
            self,
            session: AsyncSession,
    ) -> list[EventEntity]:
        """
        Извлекает все соревнования из базы данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :return: Массив соревнований, если они найдены, в противном случае - пустой массив.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = (
                select(EventModel)
            )
            result = await session.execute(stmt)
            event_models: Sequence[EventModel] = result.scalars().all()
            return [
                self.mapper.to_entity(event_model)
                for event_model in event_models
            ]
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve event: {err}"
            ) from err

    async def get_by_id(
            self,
            session: AsyncSession,
            event_id: UUID
    ) -> EventEntity | None:
        """
        Извлекает соревнование из базы данных по её id.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param event_id: Уникальный id соревнования.
        :return: Соревнование, если оно найдено, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = (
                select(EventModel)
                .where(
                    EventModel.unique_id == event_id
                )
            )
            result = await session.execute(stmt)
            event_model = result.scalar_one_or_none()
            if event_model is None:
                return None
            return self.mapper.to_entity(event_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve event by event_id '{event_id}': {err}"
            ) from err

    async def get_by_name(
            self,
            session: AsyncSession,
            event_name: str
    ) -> EventEntity | None:
        """
        Извлекает соревнование из базы данных по её названию.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param event_name: Название соревнования.
        :return: Соревнование, если оно найдено, в противном случае - None.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = (
                select(EventModel)
                .where(
                    EventModel.name == event_name
                )
            )
            result = await session.execute(stmt)
            event_model = result.scalar_one_or_none()
            if event_model is None:
                return None
            return self.mapper.to_entity(event_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve event by event_name '{event_name}': {err}"
            ) from err


    async def save(
            self,
            session: AsyncSession,
            event: EventEntity
    ) -> None:
        """
        Сохраняет новое соревнование или обновляет существующую в базе данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param event: EventEntity, которое нужно сохранить.
        :return:
        :raise RepositoryConflictError: Если во время сохранения нарушено уникальное ограничение.
        :raise RepositorySaveError: Если во время сохранения возникает ошибка базы данных.
        """
        try:
            stmt = select(EventModel).where(
                EventModel.unique_id == event.unique_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Обновите существующую модель с помощью mapper
                self.mapper.update_model_from_entity(model, event)
            else:
                # Создание новой модели с помощью mapper
                model = self.mapper.to_model(event)
            await session.merge(model)

        except IntegrityError as err:
            raise RepositoryConflictError(
                f"Conflict while saving event '{event.unique_id}': {err}"
            ) from err
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to save event '{event.unique_id}': {err}"
            ) from err
        except Exception as err:
            raise RepositorySaveError(
                f"Unexpected error while saving event '{event.unique_id}': {err}"
            ) from err

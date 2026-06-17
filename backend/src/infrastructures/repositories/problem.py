from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.problem import ProblemEntity
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError, RepositoryConflictError
from backend.src.infrastructures.mappers.problem import ProblemDBMapper
from backend.src.infrastructures.models.problem import ProblemModel


@dataclass(frozen=True, slots=True, kw_only=True)
class ProblemRepositoriesSQLAlchemy:
    """
    Реализация репозитория problem на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    Логика сопоставления делегирована ProblemDBMapper в соответствии с SRP.
    """

    mapper: ProblemDBMapper = ProblemDBMapper

    async def get_list(
            self,
            session: AsyncSession,
    ) -> list[ProblemEntity]:
        """
        Извлекает все задачи из базы данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :return: Задача, если он найдена, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(ProblemModel).options(selectinload(ProblemModel.data_sets))
            result = await session.execute(stmt)
            problem_models: Sequence[ProblemModel] = result.scalars().all()
            return [
                self.mapper.to_entity(problem_model)
                for problem_model in problem_models
            ]
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve problem: {err}"
            ) from err

    async def get_by_id(
            self,
            session: AsyncSession,
            problem_id: UUID
    ) -> ProblemEntity | None:
        """
        Извлекает задачу из базы данных по её id.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param problem_id: Уникальный id задачи.
        :return: Задача, если он найдена, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = (
                select(ProblemModel)
                .where(ProblemModel.unique_id == problem_id)
                .options(selectinload(ProblemModel.data_sets))
            )
            result = await session.execute(stmt)
            problem_model = result.scalar_one_or_none()
            if problem_model is None:
                return None
            return self.mapper.to_entity(problem_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve problem by problem_id '{problem_id}': {err}"
            ) from err

    async def get_by_name(
            self,
            session: AsyncSession,
            problem_name: str
    ) -> ProblemEntity | None:
        """
        Извлекает задачу из базы данных по её названию.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param problem_name: Название задачи.
        :return: Задача, если он найдена, в противном случае - None.
        :raise RepositoryGetError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = (
                select(ProblemModel)
                .where(ProblemModel.name == problem_name)
                .options(selectinload(ProblemModel.data_sets))
            )
            result = await session.execute(stmt)
            problem_model = result.scalar_one_or_none()
            if problem_model is None:
                return None
            return self.mapper.to_entity(problem_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve problem by problem_name '{problem_name}': {err}"
            ) from err


    async def save(
            self,
            session: AsyncSession,
            problem: ProblemEntity
    ) -> None:
        """
        Сохраняет новую задачу или обновляет существующую в базе данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param problem: ProblemEntity, которую нужно сохранить.
        :return:
        :raise RepositoryConflictError: Если во время сохранения нарушено уникальное ограничение.
        :raise RepositorySaveError: Если во время сохранения возникает ошибка базы данных.
        """
        try:
            stmt = select(ProblemModel).where(
                ProblemModel.unique_id == problem.unique_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Обновите существующую модель с помощью mapper
                self.mapper.update_model_from_entity(model, problem)
            else:
                # Создание новой модели с помощью mapper
                model = self.mapper.to_model(problem)
            session.add(model)

        except IntegrityError as err:
            raise RepositoryConflictError(
                f"Conflict while saving problem '{problem.name}': {err}"
            ) from err
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to save problem '{problem.name}': {err}"
            ) from err
        except Exception as err:
            raise RepositorySaveError(
                f"Unexpected error while saving problem '{problem.name}': {err}"
            ) from err

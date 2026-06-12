from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.team import TeamEntity
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError, RepositoryConflictError
from backend.src.infrastructures.mappers.team import TeamDBMapper
from backend.src.infrastructures.models.team import TeamModel


@dataclass(frozen=True, slots=True, kw_only=True)
class TeamRepositoriesSQLAlchemy:
    """
    Реализация репозитория team на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    Логика сопоставления делегирована TeamDBMapper в соответствии с SRP.
    """

    mapper: TeamDBMapper = TeamDBMapper

    async def get_list(
            self,
            session: AsyncSession,
    ) -> list[TeamEntity]:
        """
        Извлекает все команды из базы данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :return: Команда, если он найдена, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(TeamModel).options(selectinload(TeamModel.stages))
            result = await session.execute(stmt)
            team_models: Sequence[TeamModel] = result.scalars().all()
            return [
                self.mapper.to_entity(team_model)
                for team_model in team_models
            ]
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve team: {err}"
            ) from err

    async def get_by_id(
            self,
            session: AsyncSession,
            team_id: UUID
    ) -> TeamEntity | None:
        """
        Извлекает команду из базы данных по её id.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param team_id: Уникальный id команды.
        :return: Команда, если он найдена, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(TeamModel).where(
                TeamModel.unique_id == team_id
            ).options(selectinload(TeamModel.stages))
            result = await session.execute(stmt)
            team_model = result.scalar_one_or_none()
            if team_model is None:
                return None
            return self.mapper.to_entity(team_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve team by team_id '{team_id}': {err}"
            ) from err

    async def get_by_name(
            self,
            session: AsyncSession,
            team_name: str
    ) -> TeamEntity | None:
        """
        Извлекает команду из базы данных по её названию.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param team_name: Название команды.
        :return: Команда, если он найдена, в противном случае - None.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(TeamModel).where(
                TeamModel.name == team_name
            ).options(selectinload(TeamModel.stages))
            result = await session.execute(stmt)
            team_model = result.scalar_one_or_none()
            if team_model is None:
                return None
            return self.mapper.to_entity(team_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve team by team_id '{team_name}': {err}"
            ) from err


    async def save(
            self,
            session: AsyncSession,
            team: TeamEntity
    ) -> None:
        """
        Сохраняет новую команду или обновляет существующую в базе данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param team: TeamEntity, которую нужно сохранить.
        :return:
        :raise RepositoryConflictError: Если во время сохранения нарушено уникальное ограничение.
        :raise RepositorySaveError: Если во время сохранения возникает ошибка базы данных.
        """
        try:
            stmt = select(TeamModel).where(
                TeamModel.unique_id == team.unique_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Обновите существующую модель с помощью mapper
                self.mapper.update_model_from_entity(model, team)
            else:
                # Создание новой модели с помощью mapper
                model = self.mapper.to_model(team)
            session.add(model)

        except IntegrityError as err:
            raise RepositoryConflictError(
                f"Conflict while saving team '{team.unique_id}': {err}"
            ) from err
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to save team '{team.unique_id}': {err}"
            ) from err
        except Exception as err:
            raise RepositorySaveError(
                f"Unexpected error while saving team '{team.unique_id}': {err}"
            ) from err

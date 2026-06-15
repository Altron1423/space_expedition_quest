from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.admin import AdminEntity
from backend.src.infrastructures.exceptions import RepositoryGetError, RepositorySaveError, RepositoryConflictError
from backend.src.infrastructures.mappers.admin import AdminDBMapper
from backend.src.infrastructures.models.admin import AdminModel


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminRepositoriesSQLAlchemy:
    """
    Реализация репозитория admin на SQLAlchemy.
    Этот репозиторий отвечает только за операции с базой данных (CRUD).
    Логика сопоставления делегирована AdminDBMapper в соответствии с SRP.
    """

    mapper: AdminDBMapper = AdminDBMapper

    async def get_list(
            self,
            session: AsyncSession,
    ) -> list[AdminEntity]:
        """
        Извлекает всех админов из базы данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :return: Админа, если он найден, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(AdminModel)
            result = await session.execute(stmt)
            admin_models: Sequence[AdminModel] = result.scalars().all()
            return [
                self.mapper.to_entity(admin_model)
                for admin_model in admin_models
            ]
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve admin: {err}"
            ) from err

    async def get_by_id(
            self,
            session: AsyncSession,
            admin_id: UUID
    ) -> AdminEntity | None:
        """
        Извлекает админа из базы данных по его id.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param admin_id: Уникальный id админа.
        :return: Админ, если он найден, в противном случае - none.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(AdminModel).where(
                AdminModel.unique_id == admin_id
            )
            result = await session.execute(stmt)
            admin_model = result.scalar_one_or_none()
            if admin_model is None:
                return None
            return self.mapper.to_entity(admin_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve admin by admin_id '{admin_id}': {err}"
            ) from err

    async def get_by_name(
            self,
            session: AsyncSession,
            admin_name: str
    ) -> AdminEntity | None:
        """
        Извлекает админа из базы данных по его логину.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param admin_name: Логин админа.
        :return: Админ, если он найден, в противном случае - None.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(AdminModel).where(
                AdminModel.name == admin_name
            )
            result = await session.execute(stmt)
            admin_model = result.scalar_one_or_none()
            if admin_model is None:
                return None
            return self.mapper.to_entity(admin_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve admin by admin_name '{admin_name}': {err}"
            ) from err

    async def get_by_email(
            self,
            session: AsyncSession,
            admin_email: str
    ) -> AdminEntity | None:
        """
        Извлекает админа из базы данных по его почте.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param admin_email: Почта админа.
        :return: Админа, если он найден, в противном случае - None.
        :raise RepositorySaveError: Если во время извлечения возникает ошибка базы данных.
        """
        try:
            stmt = select(AdminModel).where(
                AdminModel.email == admin_email
            )
            result = await session.execute(stmt)
            admin_model = result.scalar_one_or_none()
            if admin_model is None:
                return None
            return self.mapper.to_entity(admin_model)
        except SQLAlchemyError as err:
            raise RepositoryGetError(
                f"Failed to retrieve admin by admin_email '{admin_email}': {err}"
            ) from err


    async def save(
            self,
            session: AsyncSession,
            admin: AdminEntity
    ) -> None:
        """
        Сохраняет новую команду или обновляет существующую в базе данных.

        :param session: AsyncSession, сессия для работы с базой данных.
        :param admin: AdminEntity, которую нужно сохранить.
        :return:
        :raise RepositoryConflictError: Если во время сохранения нарушено уникальное ограничение.
        :raise RepositorySaveError: Если во время сохранения возникает ошибка базы данных.
        """
        try:
            stmt = select(AdminModel).where(
                AdminModel.unique_id == admin.unique_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Обновите существующую модель с помощью mapper
                self.mapper.update_model_from_entity(model, admin)
            else:
                # Создание новой модели с помощью mapper
                model = self.mapper.to_model(admin)
            session.add(model)

        except IntegrityError as err:
            raise RepositoryConflictError(
                f"Conflict while saving admin '{admin.unique_id}': {err}"
            ) from err
        except SQLAlchemyError as err:
            raise RepositorySaveError(
                f"Failed to save admin '{admin.unique_id}': {err}"
            ) from err
        except Exception as err:
            raise RepositorySaveError(
                f"Unexpected error while saving admin '{admin.unique_id}': {err}"
            ) from err

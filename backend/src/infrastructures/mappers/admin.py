from dataclasses import dataclass
from typing import final

from backend.src.domain.entities.admin import AdminEntity
from backend.src.infrastructures.models.admin import AdminModel
from domain.value_objects.email_user import UserEmail
from domain.value_objects.password import UserPassword


@final
@dataclass(frozen=True, slots=True)
class AdminDBMapper:
    """
    Средство отображения для преобразования между AdminEntity (Domain) и AdminModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @staticmethod
    def to_entity(model: AdminModel) -> AdminEntity:
        """
        Преобразует SQLAlchemy AdminModel в Domain AdminEntity.

        :param model: Экземпляр SQLAlchemy AdminModel.

        :return: сущность Domain  AdminEntity.
        """
        return AdminEntity(
            unique_id=model.unique_id,
            name=model.name,
            password=UserPassword(value=model.password),
            email=UserEmail(value=model.email)
        )

    @staticmethod
    def to_model(entity: AdminEntity) -> AdminModel:
        """
        Преобразует Domain AdminEntity в SQLAlchemy AdminModel

        :param entity: сущность Domain AdminEntity.

        :return: Экземпляр SQLAlchemy AdminModel.
        """
        return AdminModel(
            unique_id=entity.unique_id,
            name=entity.name,
            password=str(entity.password),
            email=str(entity.email)
        )

    @staticmethod
    def update_model_from_entity(
        model: AdminModel, entity: AdminEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy AdminModel данными из Domain AdminEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy AdminModel для обновления.
        :param entity: Объект домена AdminEntity, содержащий новые данные.
        """
        model.name = entity.name
        model.password=str(entity.password)
        model.email=str(entity.email)

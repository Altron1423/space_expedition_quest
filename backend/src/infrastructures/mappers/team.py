from dataclasses import dataclass
from typing import final

from backend.src.domain.entities.team import TeamEntity
from backend.src.infrastructures.mappers.data_set import DataSetDBMapper
from backend.src.infrastructures.models.team import TeamModel
from domain.value_objects.email_user import UserEmail
from domain.value_objects.password import UserPassword
from infrastructures.mappers.stage import StageDBMapper


@final
@dataclass(frozen=True, slots=True)
class TeamDBMapper:
    """
    Средство отображения для преобразования между TeamEntity (Domain) и TeamModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(self, model: TeamModel) -> TeamEntity:
        """
        Преобразует SQLAlchemy TeamModel в Domain TeamEntity.

        :param model: Экземпляр SQLAlchemy TeamModel.

        :return: сущность Domain  TeamEntity.
        """
        return TeamEntity(
            unique_id=model.unique_id,
            name=model.name,
            password=UserPassword(value=model.password),
            email=UserEmail(value=model.email),
            stages=[
                StageDBMapper.to_entity(stage)
                for stage in model.stages
            ]
        )

    @classmethod
    def to_model(self, entity: TeamEntity) -> TeamModel:
        """
        Преобразует Domain TeamEntity в SQLAlchemy TeamModel

        :param entity: сущность Domain TeamEntity.

        :return: Экземпляр SQLAlchemy TeamModel.
        """
        return TeamModel(
            unique_id=entity.unique_id,
            name=entity.name,
            password=str(entity.password),
            email=str(entity.email),
            stages=[
                StageDBMapper.to_model(stage)
                for stage in entity.stages
            ]
        )

    @classmethod
    def update_model_from_entity(
        cls, model: TeamModel, entity: TeamEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy TeamModel данными из Domain TeamEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy TeamModel для обновления.
        :param entity: Объект домена TeamEntity, содержащий новые данные.
        """
        model.name = entity.name
        model.text = entity.text
        model.data_set = [
            DataSetDBMapper.to_model(dset)
            for dset in entity.data_sets
        ]

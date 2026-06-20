from dataclasses import dataclass
from datetime import UTC
from typing import final

from backend.src.domain.entities.team import TeamEntity
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
            work_problem_id=model.work_problem_id,
            work_data_set_id=model.work_data_set_id,
            stage_now=model.stage_now,
            start_stage=model.start_stage.replace(tzinfo=UTC),
            event_id=model.event_id,
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
            work_problem_id=entity.work_problem_id,
            work_data_set_id=entity.work_data_set_id,
            stage_now=entity.stage_now,
            start_stage=entity.start_stage,
            event_id=entity.event_id,
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
        model.event_id = entity.event_id
        model.password = str(entity.password)
        model.email = str(entity.email)
        model.work_problem_id = entity.work_problem_id
        model.work_data_set_id = entity.work_data_set_id
        model.stage_now = entity.stage_now
        model.start_stage = entity.start_stage
        model.stages = [
            StageDBMapper.to_model(stage)
            for stage in entity.stages
        ]

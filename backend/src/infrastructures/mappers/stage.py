from dataclasses import dataclass
from typing import final

from backend.src.domain.entities.stage import StageEntity
from backend.src.infrastructures.mappers.data_set import DataSetDBMapper
from backend.src.infrastructures.models.stage import StageModel
from infrastructures.mappers.problem import ProblemDBMapper


@final
@dataclass(frozen=True, slots=True)
class StageDBMapper:
    """
    Средство отображения для преобразования между StageEntity (Domain) и StageModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(cls, model: StageModel) -> StageEntity:
        """
        Преобразует SQLAlchemy StageModel в Domain StageEntity.

        :param model: Экземпляр SQLAlchemy StageModel.

        :return: сущность Domain  StageEntity.
        """
        return StageEntity(
            unique_id=model.unique_id,
            stage=model.stage,
            problem=ProblemDBMapper.to_entity(model.problem),
            data_set=DataSetDBMapper.to_entity(model.data_set),
            duration=model.duration,
        )

    @classmethod
    def to_model(cls, entity: StageEntity) -> StageModel:
        """
        Преобразует Domain StageEntity в SQLAlchemy StageModel

        :param entity: сущность Domain StageEntity.

        :return: Экземпляр SQLAlchemy StageModel.
        """
        return StageModel(
            unique_id=entity.unique_id,
            stage=entity.stage,
            problem=ProblemDBMapper.to_model(entity.problem),
            data_set=DataSetDBMapper.to_model(entity.data_set),
            duration=entity.duration,
        )

    @classmethod
    def update_model_from_entity(
        cls, model: StageModel, entity: StageEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy StageModel данными из Domain StageEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy StageModel для обновления.
        :param entity: Объект домена StageEntity, содержащий новые данные.
        """
        model.stage = entity.stage
        model.problem = ProblemDBMapper.to_model(entity.problem)
        model.data_set = DataSetDBMapper.to_model(entity.data_set)
        model.duration = entity.duration

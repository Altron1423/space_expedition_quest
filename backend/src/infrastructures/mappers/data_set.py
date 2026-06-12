from dataclasses import dataclass
from typing import final
from uuid import UUID

from backend.src.application.dtos.problem import (
    DataSetDTO
)

from backend.src.domain.entities.problem import DataSetEntity
from backend.src.infrastructures.models.problem import DataSetModel



@final
@dataclass(frozen=True, slots=True)
class InfrastructureDataSetMapper:
    """
    Средство отображения для преобразования Application DTOs в
    словари для взаимодействия с внешним API.
    """

    def to_dict(self, dto: DataSetDTO) -> dict:
        """
        Преобразует приложение DataSetDto в словарь для сериализации в формате JSON
        (например, кэширование, внешние API).
        """
        return {
            "unique_id": str(dto.unique_id),
            "problem": str(dto.problem),
            "elements": dto.elements,
            "answer": dto.answer
        }

    def from_dict(self, data: dict) -> DataSetDTO:
        """
        Преобразует словарь из JSON-десериализации в приложение DataSetDto.
        """
        return DataSetDTO(
            unique_id=UUID(data["unique_id"]),
            problem=UUID(data["problem"]),
            elements=data["elements"],
            answer=data["answer"]
        )

@final
@dataclass(frozen=True, slots=True)
class DataSetDBMapper:
    """
    Средство отображения для преобразования между DataSetEntity (Domain) и DataSetModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(self, model: DataSetModel) -> DataSetEntity:
        """
        Преобразует SQLAlchemy DataSetModel в Domain DataSetEntity.

        :param model: Экземпляр SQLAlchemy DataSetModel.

        :return: сущность Domain DataSetEntity.
        """
        return DataSetEntity(
            unique_id=model.unique_id,
            problem=model.problem,
            elements=model.element,
            answer=model.answer
        )

    @classmethod
    def to_model(self, entity: DataSetEntity) -> DataSetModel:
        """
        Преобразует Domain DataSetEntity в SQLAlchemy DataSetModel

        :param entity: сущность Domain DataSetEntity.

        :return: Экземпляр SQLAlchemy DataSetModel.
        """
        return DataSetModel(
            unique_id=entity.unique_id,
            problem=entity.problem,
            element=entity.elements,
            answer=entity.answer
        )

    @classmethod
    def update_model_from_entity(
        cls, model: DataSetModel, entity: DataSetEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy DataSetModel данными из Domain DataSetEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy DataSetModel для обновления.
        :param entity: Объект домена DataSetEntity, содержащий новые данные.
        """
        model.elements = entity.elements
        model.answer = entity.answer

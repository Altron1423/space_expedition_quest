from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID

from backend.src.application.dtos.example import (
    ExampleDTO,
    SizeDTO,
)

from backend.src.domain.entities.example import ExampleEntity
from backend.src.domain.value_objects.example_size import ExampleSize
from backend.src.infrastructures.models.example import ExampleModel



@final
@dataclass(frozen=True, slots=True)
class InfrastructureExampleMapper:
    """
    Средство отображения для преобразования Application DTOs в
    словари для взаимодействия с внешним API.
    """

    def to_dict(self, dto: ExampleDTO) -> dict:
        """
        Преобразует приложение ExampleDto в словарь для сериализации в формате JSON
        (например, кэширование, внешние API).
        """
        return {
            "unique_id": str(dto.unique_id),
            "created_at": dto.created_at.isoformat(),
            "name": dto.name,
            "size": {"value": dto.size.value},
            "description": dto.description,
        }

    def from_dict(self, data: dict) -> ExampleDTO:
        """
        Преобразует словарь из JSON-десериализации в приложение ExampleDto.
        """
        return ExampleDTO(
            unique_id=UUID(data["unique_id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            name=data["name"],
            size=SizeDTO(value=data["size"]["value"]),
            description=data.get("description"),
        )

@final
@dataclass(frozen=True, slots=True)
class ExampleDBMapper:
    """
    Средство отображения для преобразования между ExampleEntity (Domain) и ExampleModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(self, model: ExampleModel) -> ExampleEntity:
        """
        Преобразует SQLAlchemy ExampleModel в Domain ExampleEntity.

        :param model: Экземпляр SQLAlchemy ExampleModel.

        :return: сущность Domain  ExampleEntity.
        """
        return ExampleEntity(
            unique_id=model.unique_id,
            name=model.name,
            created_at=model.created_at,
            size=ExampleSize(value=model.size),
            description=model.description,
        )

    @classmethod
    def to_model(self, entity: ExampleEntity) -> ExampleModel:
        """
        Преобразует Domain ExampleEntity в SQLAlchemy ExampleModel

        :param entity: сущность Domain ExampleEntity.

        :return: Экземпляр SQLAlchemy ExampleModel.
        """
        return ExampleModel(
            unique_id=entity.unique_id,
            name=entity.name,
            created_at=entity.created_at,
            size=str(entity.size),
            description=entity.description,
        )

    @classmethod
    def update_model_from_entity(
        cls, model: ExampleModel, entity: ExampleEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy ExampleModel данными из Domain ExampleEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy ExampleModel для обновления.
        :param entity: Объект домена ExampleEntity, содержащий новые данные.
        """
        model.name = entity.name
        model.size = str(entity.size)
        model.description = entity.description

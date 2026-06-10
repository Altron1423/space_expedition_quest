from dataclasses import dataclass
from typing import final
from uuid import UUID

from backend.src.application.dtos.example import (
    ExampleDTO,
    SizeDTO,
)


from backend.src.domain.entities.example import ExampleEntity

from backend.src.domain.value_objects.example_size import ExampleSize

@final
@dataclass(frozen=True, slots=True)
class ExampleMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_dto(entity: ExampleEntity) -> ExampleDTO:
        """
        Преобразуйте Domain Entity в Application DTO.
        """
        return ExampleDTO(
            unique_id=entity.unique_id,
            created_at=entity.created_at,
            name=entity.name,
            size=SizeDTO(value=entity.size.value),
            description=entity.description,
        )

    @staticmethod
    def to_entity(dto: ExampleDTO) -> ExampleEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return ExampleEntity(
            unique_id=dto.unique_id,
            name=dto.name,
            size=ExampleSize(value=dto.size.value),
            description=dto.description,
        )

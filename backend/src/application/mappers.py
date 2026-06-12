from dataclasses import dataclass
from typing import final

from backend.src.application.dtos.example import (
    ExampleDTO,
    SizeDTO,
)
from backend.src.application.dtos.problem import ProblemDTO, DataSetDTO, CreateProblemDTO
from backend.src.application.exceptions import CreateProblemUuidIsNone
from backend.src.domain.entities.data_set import DataSetEntity

from backend.src.domain.entities.example import ExampleEntity
from backend.src.domain.entities.problem import ProblemEntity

from backend.src.domain.value_objects.example_size import ExampleSize

@final
@dataclass(frozen=True, slots=True)
class DataSetMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_dto(entity: DataSetEntity) -> DataSetDTO:
        """
        Преобразуйте Domain Entity в Application DTO.
        """
        return DataSetDTO(
            unique_id=entity.unique_id,
            problem=entity.problem,
            elements=entity.elements,
            answer=entity.answer,
        )

    @staticmethod
    def to_entity(dto: DataSetDTO) -> DataSetEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return DataSetEntity(
            unique_id=dto.unique_id,
            problem=dto.problem,
            elements=dto.elements,
            answer=dto.answer,
        )

@final
@dataclass(frozen=True, slots=True)
class ProblemMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_dto(entity: ProblemEntity) -> ProblemDTO:
        """
        Преобразуйте Domain Entity в Application DTO.
        """
        return ProblemDTO(
            unique_id=entity.unique_id,
            name=entity.name,
            text=entity.text,
            data_sets=[
                DataSetMapper.to_dto(dset)
                for dset in entity.data_sets
            ]
        )

    @staticmethod
    def to_entity(dto: ProblemDTO) -> ProblemEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return ProblemEntity(
            unique_id=dto.unique_id,
            name=dto.name,
            text=dto.text,
            data_sets=[
                DataSetMapper.to_entity(dset)
                for dset in dto.data_sets
            ]
        )

@final
@dataclass(frozen=True, slots=True)
class CreateProblemMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_entity(dto: CreateProblemDTO) -> ProblemEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        if dto.unique_id is None:
            raise CreateProblemUuidIsNone()
        return ProblemEntity(
            unique_id=dto.unique_id,
            name=dto.name,
            text=dto.text,
            data_sets=[
                DataSetMapper.to_entity(dset)
                for dset in dto.data_sets
            ]
        )


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

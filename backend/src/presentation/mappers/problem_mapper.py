from dataclasses import dataclass
from typing import final

from backend.src.application.dtos.problem import ProblemDTO, DataSetDTO
from backend.src.presentation.schemas.responses import (
    ProblemResponseSchema,
    ProblemsResponseSchema, DataSetResponseSchema,
)


@final
@dataclass(frozen=True, slots=True)
class DataSetPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    @classmethod
    def to_response(cls, dto: DataSetDTO) -> DataSetResponseSchema:
        """Преобразуйте Application DTO в API Response model."""

        return DataSetResponseSchema(
            unique_id=dto.unique_id,
            elements=dto.elements,
            answer=dto.answer,
        )

@final
@dataclass(frozen=True, slots=True)
class ProblemPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """
    mapper = DataSetPresentationMapper

    @classmethod
    def to_response(cls, dto: ProblemDTO) -> ProblemResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        data_sets: list[DataSetResponseSchema] = []
        for i_data_set in dto.data_sets:
            data_sets.append(
                cls.mapper.to_response(i_data_set)
            )

        return ProblemResponseSchema(
            unique_id=dto.unique_id,
            name=dto.name,
            text=dto.text,
            data_sets=data_sets,
        )

@final
@dataclass(frozen=True, slots=True)
class ProblemsPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    mapper = ProblemPresentationMapper

    @classmethod
    def to_response(cls, dto: list[ProblemDTO]) -> ProblemsResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        problems = []
        for i_dto in dto:
            problems.append(
                cls.mapper.to_response(i_dto)
            )
        return ProblemsResponseSchema(
            problems=problems
        )
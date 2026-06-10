from dataclasses import dataclass
from typing import final

from backend.src.application.dtos.example import ExampleDTO
from backend.src.presentation.schemas.responses import (
    ExampleResponseSchema
)


@final
@dataclass(frozen=True, slots=True)
class ExamplePresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    @classmethod
    def to_response(cls, dto: ExampleDTO) -> ExampleResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        return ExampleResponseSchema(
            unique_id=dto.unique_id,
            created_at=dto.created_at,
            name=dto.name,
            description=dto.description,
        )
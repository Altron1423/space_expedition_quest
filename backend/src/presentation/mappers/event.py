from dataclasses import dataclass
from typing import final

from backend.src.application.dtos.event import EventDTO
from backend.src.presentation.schemas.responses import (
    EventResponseSchema,
    EventsResponseSchema,
)

@final
@dataclass(frozen=True, slots=True)
class EventPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """
    @classmethod
    def to_response(cls, dto: EventDTO) -> EventResponseSchema:
        """Преобразуйте Application DTO в API Response model."""

        return EventResponseSchema(
            unique_id=dto.unique_id,
            name=dto.name,
            description=dto.description,
            location=dto.location,
            date=dto.date,
        )

@final
@dataclass(frozen=True, slots=True)
class EventsPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    mapper = EventPresentationMapper

    @classmethod
    def to_response(cls, dto: list[EventDTO]) -> EventsResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        return EventsResponseSchema(
            events=[
                cls.mapper.to_response(i_dto)
                for i_dto in dto
            ]
        )
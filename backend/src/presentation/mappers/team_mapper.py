from dataclasses import dataclass
from typing import final

from application.dtos.stage import StageDTO
from application.dtos.team import TeamDTO
from backend.src.presentation.schemas.responses import (
    StageResponseSchema,
    TeamResponseSchema, TeamsResponseSchema,
)
from presentation.mappers.problem_mapper import ProblemPresentationMapper, DataSetPresentationMapper
from presentation.schemas.responses import DataSetResponseSchema


@final
@dataclass(frozen=True, slots=True)
class StagePresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    @classmethod
    def to_response(cls, dto: StageDTO) -> StageResponseSchema:
        """Преобразуйте Application DTO в API Response model."""

        return StageResponseSchema(
            unique_id=dto.unique_id,
            stage=dto.stage,
            problem=ProblemPresentationMapper.to_response(dto.problem),
            data_set=DataSetPresentationMapper.to_response(dto.data_set),
            answer=dto.answer,
            duration=dto.duration,
        )

@final
@dataclass(frozen=True, slots=True)
class TeamPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """
    mapper = StagePresentationMapper

    @classmethod
    def to_response(cls, dto: TeamDTO) -> TeamResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        stages: list[StageResponseSchema] = []
        for i_data_set in dto.stages:
            stages.append(
                cls.mapper.to_response(i_data_set)
            )

        return TeamResponseSchema(
            unique_id=dto.unique_id,
            name=dto.name,
            email=str(dto.email),
            stages=stages
        )

@final
@dataclass(frozen=True, slots=True)
class TeamsPresentationMapper:
    """
    Средство отображения для преобразования Application DTOs в Presentation Response models.

    Это средство отображения изолирует уровень представления от прямых зависимостей от Application DTOs,
    в соответствии с принципами чистой архитектуры.
    """

    mapper = TeamPresentationMapper

    @classmethod
    def to_response(cls, dto: list[TeamDTO]) -> TeamsResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        teams = []
        for i_dto in dto:
            teams.append(
                cls.mapper.to_response(i_dto)
            )
        return TeamsResponseSchema(
            teams=teams
        )
from dataclasses import dataclass
from typing import final

from backend.src.domain.entities.event import EventEntity

from backend.src.infrastructures.models.event import EventModel
from backend.src.infrastructures.mappers.problem import ProblemDBMapper
from backend.src.infrastructures.mappers.team import TeamDBMapper


# @final
# @dataclass(frozen=True, slots=True)
# class InfrastructureEventMapper:
#     """
#     Средство отображения для преобразования Application DTOs в
#     словари для взаимодействия с внешним API.
#     """
#
#     def to_dict(self, dto: EventDTO) -> dict:
#         """
#         Преобразует приложение EventDto в словарь для сериализации в формате JSON
#         (например, кэширование, внешние API).
#         """
#         return {
#             "unique_id": str(dto.unique_id),
#             "name": dto.name,
#             "text": dto.text,
#             "data_set": dto.data_set,
#             "answer": dto.answer
#         }
#
#     def from_dict(self, data: dict) -> EventDTO:
#         """
#         Преобразует словарь из JSON-десериализации в приложение EventDto.
#         """
#         return EventDTO(
#             unique_id=UUID(data["unique_id"]),
#             name=data["name"],
#             text=data["text"],
#             data_sets=data["data_sets"]
#         )

@final
@dataclass(frozen=True, slots=True)
class EventDBMapper:
    """
    Средство отображения для преобразования между EventEntity (Domain) и EventModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(cls, model: EventModel) -> EventEntity:
        """
        Преобразует SQLAlchemy EventModel в Domain EventEntity.

        :param model: Экземпляр SQLAlchemy EventModel.

        :return: сущность Domain  EventEntity.
        """
        return EventEntity(
            unique_id=model.unique_id,
            name=model.name,
            description=model.description,
            location=model.location,
            date=model.date,
            teams=[
                TeamDBMapper.to_entity(team)
                for team in model.teams
            ],
            problems=[
                ProblemDBMapper.to_entity(problem)
                for problem in model.problems
            ],
        )

    @classmethod
    def to_model(cls, entity: EventEntity) -> EventModel:
        """
        Преобразует Domain EventEntity в SQLAlchemy EventModel

        :param entity: сущность Domain EventEntity.

        :return: Экземпляр SQLAlchemy EventModel.
        """
        return EventModel(
            unique_id=entity.unique_id,
            name=entity.name,
            description=entity.description,
            location=entity.location,
            date=entity.date,
            teams=[
                TeamDBMapper.to_model(team)
                for team in entity.teams
            ],
            problems=[
                ProblemDBMapper.to_model(problem)
                for problem in entity.problems
            ],
        )

    @classmethod
    def update_model_from_entity(
        cls, model: EventModel, entity: EventEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy EventModel данными из Domain EventEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy EventModel для обновления.
        :param entity: Объект домена EventEntity, содержащий новые данные.
        """
        model.name = entity.name
        model.description = entity.description
        model.location = entity.location
        model.date = entity.date
        model.teams = [
            TeamDBMapper.to_model(team)
            for team in entity.teams
        ]
        model.problems = [
            ProblemDBMapper.to_model(problem)
            for problem in entity.problems
        ]

from dataclasses import dataclass
from typing import final
from backend.src.domain.entities.problem import ProblemEntity
from backend.src.infrastructures.mappers.data_set import DataSetDBMapper
from backend.src.infrastructures.models.problem import ProblemModel



# @final
# @dataclass(frozen=True, slots=True)
# class InfrastructureProblemMapper:
#     """
#     Средство отображения для преобразования Application DTOs в
#     словари для взаимодействия с внешним API.
#     """
#
#     def to_dict(self, dto: ProblemDTO) -> dict:
#         """
#         Преобразует приложение ProblemDto в словарь для сериализации в формате JSON
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
#     def from_dict(self, data: dict) -> ProblemDTO:
#         """
#         Преобразует словарь из JSON-десериализации в приложение ProblemDto.
#         """
#         return ProblemDTO(
#             unique_id=UUID(data["unique_id"]),
#             name=data["name"],
#             text=data["text"],
#             data_sets=data["data_sets"]
#         )

@final
@dataclass(frozen=True, slots=True)
class ProblemDBMapper:
    """
    Средство отображения для преобразования между ProblemEntity (Domain) и ProblemModel (SQLAlchemy).

    Этот класс предоставляет методы для двунаправленного отображения, обеспечивая разделение задач
    между логикой домена и сохранением базы данных.
    """

    @classmethod
    def to_entity(self, model: ProblemModel) -> ProblemEntity:
        """
        Преобразует SQLAlchemy ProblemModel в Domain ProblemEntity.

        :param model: Экземпляр SQLAlchemy ProblemModel.

        :return: сущность Domain  ProblemEntity.
        """
        return ProblemEntity(
            unique_id=model.unique_id,
            name=model.name,
            text=model.text,
            data_sets=[
                DataSetDBMapper.to_entity(dset)
                for dset in model.data_sets
            ]
        )

    @classmethod
    def to_model(self, entity: ProblemEntity) -> ProblemModel:
        """
        Преобразует Domain ProblemEntity в SQLAlchemy ProblemModel

        :param entity: сущность Domain ProblemEntity.

        :return: Экземпляр SQLAlchemy ProblemModel.
        """
        return ProblemModel(
            unique_id=entity.unique_id,
            name=entity.name,
            text=entity.text,
            data_sets=[
                DataSetDBMapper.to_model(dset)
                for dset in entity.data_sets
            ]
        )

    @classmethod
    def update_model_from_entity(
        cls, model: ProblemModel, entity: ProblemEntity
    ) -> None:
        """
        Обновляет существующую SQLAlchemy ProblemModel данными из Domain ProblemEntity.

        Этот метод используется для обновления записей базы данных на основе изменений в доменной сущности.

        :param model: Существующая SQLAlchemy ProblemModel для обновления.
        :param entity: Объект домена ProblemEntity, содержащий новые данные.
        """
        model.name = entity.name
        model.text = entity.text
        model.data_set = [
            DataSetDBMapper.to_model(dset)
            for dset in entity.data_sets
        ]

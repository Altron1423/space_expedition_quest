from dataclasses import dataclass
from typing import final
from uuid import uuid4

from application.dtos.email import EmailDTO
from application.dtos.password import PasswordDTO
from application.dtos.stage import StageDTO
from application.dtos.team import TeamDTO, CreateTeamDTO
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
from domain.entities.stage import StageEntity
from domain.entities.team import TeamEntity
from domain.value_objects.email_user import UserEmail
from domain.value_objects.password import UserPassword


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
class StageMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_dto(entity: StageEntity) -> StageDTO:
        """
        Преобразуйте Domain Entity в Application DTO.
        """
        return StageDTO(
            unique_id=entity.unique_id,
            stage=entity.stage,
            problem=ProblemMapper.to_dto(entity.problem),
            data_set=DataSetMapper.to_dto(entity.data_set),
            duration=entity.duration,
        )

    @staticmethod
    def to_entity(dto: StageDTO) -> StageEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return StageEntity(
            unique_id=dto.unique_id,
            stage=dto.stage,
            problem=ProblemMapper.to_entity(dto.problem),
            data_set=DataSetMapper.to_entity(dto.data_set),
            duration=dto.duration,
        )

@final
@dataclass(frozen=True, slots=True)
class TeamMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_dto(entity: TeamEntity) -> TeamDTO:
        """
        Преобразуйте Domain Entity в Application DTO.
        """
        return TeamDTO(
            unique_id=entity.unique_id,
            name=entity.name,
            password=PasswordDTO(value=entity.password.value),
            email=EmailDTO(value=entity.email.value),
            stages=[
                StageMapper.to_dto(dset)
                for dset in entity.stages
            ]
        )

    @staticmethod
    def to_entity(dto: TeamDTO) -> TeamEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return TeamEntity(
            unique_id=dto.unique_id,
            name=dto.name,
            password=UserPassword(value=dto.password.value),
            email=UserEmail(value=dto.email.value),
            stages=[
                StageMapper.to_entity(dset)
                for dset in dto.stages
            ]
        )

@final
@dataclass(frozen=True, slots=True)
class CreateTeamMapper:
    """
    Средство отображения для преобразования между Domain Entities и Application DTOs.

    Это средство отображения является частью прикладного уровня и обрабатывает преобразования между:
    - Domain Entities (бизнес-логика)
    - Application DTO (передача данных по сценарию использования)

    Оно не решает проблемы инфраструктуры, такие как сериализация JSON.
    """

    @staticmethod
    def to_entity(dto: CreateTeamDTO) -> TeamEntity:
        """
        Преобразуйте Application DTO в Domain Entity.
        """
        return TeamEntity(
            unique_id=uuid4(),
            name=dto.name,
            password=UserPassword(value="qwerty"),
            email=UserEmail(value=dto.email.value),
            stages=[]
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

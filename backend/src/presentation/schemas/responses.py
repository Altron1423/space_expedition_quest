from datetime import datetime, timedelta
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class ExampleResponseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )

    unique_id: UUID = Field(..., description="Уникальный идентификатор example")
    created_at: datetime = Field(
        description="Временная метка, когда была создана запись example (UTC)",
    )
    name: str = Field(..., description="Название example")
    description: str | None = Field(
        None, description="Необязательное описание example"
    )


class DataSetResponseSchema(BaseModel):
    unique_id: UUID = Field(..., description="Уникальный идентификатор набора данных")
    elements: list[str] = Field(..., description="Значения набора данных")
    answer: str = Field(..., description="Ответ для данных значений")

class ProblemResponseSchema(BaseModel):
    unique_id: UUID = Field(..., description="Уникальный идентификатор задачи")
    name: str = Field(..., description="Название задачи")
    text: str = Field(..., description="Текст задачи")
    data_sets: list[DataSetResponseSchema] = Field(..., description="Варианты наборов значений с ответами для задач")

class ProblemsResponseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )
    problems: list[ProblemResponseSchema] = Field(description="Задачи")



class StageResponseSchema(BaseModel):
    unique_id: UUID = Field(..., description="Уникальный идентификатор набора данных")
    stage: int = Field(..., description="Номер испытания")
    problem: ProblemResponseSchema = Field(..., description="Условия решённой задачи")
    data_set: DataSetResponseSchema = Field(..., description="Данные решённой задачи")
    answer: str = Field(..., description="Ответ команды")
    duration: timedelta = Field(..., description="Время затраченное на решение")

class TeamResponseSchema(BaseModel):
    unique_id: UUID = Field(..., description="Уникальный идентификатор задачи")
    name: str = Field(..., description="Название задачи")
    email: EmailStr = Field(..., description="Email команды")
    stages: list[StageResponseSchema] = Field(..., description="Текст задачи")

class TeamsResponseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )
    teams: list[TeamResponseSchema] = Field(description="Команды")


class EventResponseSchema(BaseModel):
    unique_id: UUID = Field(..., description="Уникальный идентификатор задачи")
    name: str = Field(..., description="Название соревнования")
    description: str = Field(..., description="Описание соревнования")
    location: str = Field(..., description="Место проведения соревнования")
    date: datetime = Field(..., description="Описание соревнования")

class EventsResponseSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )
    events: list[EventResponseSchema] = Field(description="Соревнования")



class TokenResponseSchema(BaseModel):
    """
    Содержит результат авторизации, access token и refresh token.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )
    ok: bool = Field(..., description="Результат получения токенов")
    access_token: str = Field(..., description="Рабочий токен")
    refresh_token: str = Field(..., description="Токенов для обновления")


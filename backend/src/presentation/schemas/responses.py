from datetime import datetime
from typing import List
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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



class UserTokenResponseSchema(BaseModel):
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


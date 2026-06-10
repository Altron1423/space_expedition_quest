from datetime import datetime
from typing import List
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductResponse(BaseModel):
    unique_id: UUID
    title: str
    description: str
    price: Decimal
    category: str
    owner_id: UUID
    owner_username: str
    created_at: datetime

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


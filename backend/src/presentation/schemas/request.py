import re

from pydantic import BaseModel, EmailStr, ConfigDict, Field, validator

from decimal import Decimal

from backend.src.presentation.exceptions import PasswordError


class BaseRequest(BaseModel):
    """Базовый класс для всех запросов"""
    model_config = ConfigDict(
        extra="forbid",  # Запрещаем дополнительные поля
        populate_by_name=True,
        json_schema_extra={}
    )


class PasswordSchema(BaseModel):
    """
    Схема валидации пароля для переиспользования
    """

    value: str = Field(
        ...,
        description="Пароль (минимум 8 символов, должен содержать заглавные, строчные буквы и цифры)",
        min_length=8,
        max_length=100,
        examples=["StrongP@ssw0rd"]
    )

    @validator('value')
    def password_strength(cls, v):
        """Проверка сложности пароля"""
        errors = []

        # Проверка на заглавные буквы
        if not re.search(r'[A-ZА-Я]', v):
            errors.append('должен содержать хотя бы одну заглавную букву')

        # Проверка на строчные буквы
        if not re.search(r'[a-zа-я]', v):
            errors.append('должен содержать хотя бы одну строчную букву')

        # Проверка на цифры
        if not re.search(r'\d', v):
            errors.append('должен содержать хотя бы одну цифру')

        # Проверка на специальные символы
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            errors.append('должен содержать хотя бы один специальный символ')

        if errors:
            raise PasswordError(f'Пароль {", ".join(errors)}')

        return v


class AdminRegisterRequest(BaseRequest):
    """
    Запрос на регистрацию нового администратора

    Пример:
    {
        "username": "Иван",
        "email": "user@example.com",
        "password": {
            "value": "StrongP@ssw0rd"
        }
    }
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван",
                "email": "user@example.com",
                "password": {
                    "value": "StrongP@ssw0rd"
                }
            }
        }
    )
    name: str = Field(
        ...,
        description="Имя пользователя",
        min_length=2,
        max_length=50,
        examples=["Иван", "John"]
    )

    email: EmailStr = Field(
        ...,
        description="Email пользователя",
        examples=["user@example.com", "john.doe@gmail.com"]
    )

    password: PasswordSchema = Field(..., description="Пароль")


    @validator('name')
    def validate_name(cls, v):
        """Валидация имени и фамилии"""
        if not v.replace('-', '').replace(' ', '').isalpha():
            raise ValueError('Имя должно содержать только буквы, пробелы и дефисы')
        return v.strip().title()

class TeamRegisterRequest(BaseRequest):
    """
    Запрос на регистрацию нового пользователя

    Пример:
    {
        "username": "Иван",
        "email": "user@example.com",
        "password": {
            "value": "StrongP@ssw0rd"
        },
        "accept_terms": True
    }
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван",
                "email": "user@example.com"
            }
        }
    )
    name: str = Field(
        ...,
        description="Имя пользователя",
        min_length=2,
        max_length=50,
        examples=["Иван", "John"]
    )

    email: EmailStr = Field(
        ...,
        description="Email пользователя",
        examples=["user@example.com", "john.doe@gmail.com"]
    )

    @validator('name')
    def validate_name(cls, v):
        """Валидация имени и фамилии"""
        if not v.replace('-', '').replace(' ', '').isalpha():
            raise ValueError('Название должно содержать только буквы, пробелы и дефисы')
        return v.strip().title()


class AdminLoginRequest(BaseRequest):
    """
    Запрос на вход администратора
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": {
                    "value": "StrongP@ssw0rd"
                }
            }
        }
    )

    email: EmailStr = Field(
        ...,
        description="Email пользователя",
        examples=["user@example.com", "john.doe@gmail.com"]
    )

    password: PasswordSchema = Field(..., description="Пароль")


class TeamLoginRequest(BaseRequest):
    """
    Запрос на вход команды
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Team",
                "password": {
                    "value": "StrongP@ssw0rd"
                }
            }
        }
    )

    name: str = Field(..., description="Название пользователя")

    password: PasswordSchema = Field(..., description="Пароль")


class DataSetRequest(BaseRequest):
    elements: list[str] = Field(min_length=1, max_length=50, description="Значения, подставляемые в задачу")
    answer: str = Field(min_length=1, max_length=200, description="Целевой ответ")

class CreateProblemRequest(BaseRequest):
    name: str = Field(min_length=1, max_length=50, description="Название задачи")
    text: str = Field(min_length=1, max_length=1000, description="Условие задачи")
    data_set: list[DataSetRequest] = Field(..., description="Наборы данных")

class CreateTeamRequest(BaseRequest):
    name: str = Field(min_length=1, max_length=50, description="Название команды")
    email: EmailStr = Field(
        ...,
        description="Email пользователя",
        examples=["user@example.com", "john.doe@gmail.com"]
    )

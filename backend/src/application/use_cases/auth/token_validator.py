import enum
import json
import time
from typing import Literal

import structlog


from uuid import UUID
from authx import exceptions
from fastapi import HTTPException, Request


from backend.src.application.exceptions import MissingAccessJWTTokenError, AccessJWTDecodeError
from backend.src.application.security.jwt_security import security

from backend.src.domain.entities.admin import AdminEntity
from backend.src.domain.entities.team import TeamEntity

from backend.src.infrastructures.repositories.admin import AdminRepositoriesSQLAlchemy
from backend.src.infrastructures.repositories.team import TeamRepositoriesSQLAlchemy
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy

logger = structlog.get_logger(__name__)


dict_users_rec = {}
max_user_rec = 1000
min_time_user_rec = 0

uow: UnitOfWorkSQLAlchemy = UnitOfWorkSQLAlchemy()


def valid_time_count_request(request_client):
    client = request_client
    # print(client)

    if client not in dict_users_rec:
        dict_users_rec[client] = [1, time.time()]
    else:
        # print(time.time() - dict_users_rec[client][1])
        if time.time() - dict_users_rec[client][1] < min_time_user_rec:
            dict_users_rec[client][1] = time.time()
            raise HTTPException(status_code=429, detail=f"You can't send requests that often.")

        dict_users_rec[client][1] = time.time()
        dict_users_rec[client][0] += 1

        # print(dict_users_rec[client] > max_user_rec, dict_users_rec[client], max_user_rec)
        if dict_users_rec[client][0] > max_user_rec:
            raise HTTPException(status_code=423, detail=f"You can't send requests.")

class StatusEnum(enum.Enum):
    zero = ""
    admin = "admin"
    team = "team"
    all = "all"
    none = "None"

async def valid_user_statuses(raw_data: str, statuses) -> AdminEntity | TeamEntity:
    async def f(uuid):
        async with uow as session:
            result = await repository.get_by_id(session, uuid)
            if result is None:
                raise HTTPException(status_code=403, detail=f"Insufficient authority")
            return result

    data = json.loads(raw_data)
    uuid = UUID(data["unique_id"])
    status = StatusEnum.none

    if data["type"] == "admin":
        repository = AdminRepositoriesSQLAlchemy()
        status = StatusEnum.admin
    elif data["type"] == "team":
        repository = TeamRepositoriesSQLAlchemy()
        status = StatusEnum.team

    if statuses == StatusEnum.all:
        return await f(uuid)

    if type(statuses) != list:
        statuses = [statuses]

    if status in statuses + [StatusEnum.zero]:
        return await f(uuid)

    raise HTTPException(status_code=403, detail=f"Insufficient authority")


async def TokenValidatorUseCase(request: Request, statuses: StatusEnum | list[StatusEnum] = StatusEnum.none) -> UUID | None:
    """
    Выполняет процесс проверки наличия и валидности jwt токена доступа.

    :param statuses: Допускаемые статусы.
    :param request: Информация пользователя.

    :return: Информация сохранённая в jwt токене: UUID пользователя, которому он был выдан.
    """

    if statuses != StatusEnum.none:
        try:
            access_payload = await security.access_token_required(request)
        except exceptions.MissingTokenError as e:
            raise MissingAccessJWTTokenError(f"Undefined token in cookie")
        except exceptions.JWTDecodeError as e:
            raise AccessJWTDecodeError(f"Invalid token or the access token has expired.")

        valid_time_count_request(request.client)

        entity = await valid_user_statuses(access_payload.sub, statuses)

        return entity.unique_id

    valid_time_count_request(request.client)
    return None

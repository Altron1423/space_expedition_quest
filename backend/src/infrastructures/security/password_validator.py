import os

from authx import AuthX, AuthXConfig, exceptions
from fastapi import HTTPException, Request

from backend.src.infrastructures.exceptions import MissingJWTTokenError, JWTDecodeError

config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "access_token_KGU"
config.JWT_REFRESH_COOKIE_NAME = "refresh_token_KGU"
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_TOKEN_LOCATION = ["headers", "query", "cookies", "json"]
# config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = "HS256"
# config.JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=20)


security = AuthX(config=config)


# async def user_request_validity(request, statuses: StatusEnum | list[StatusEnum] = None, session=None):
#     # valid_time_count_request(request)
#
#     if not statuses is None:
#         data = await valid_token(request)
#
#         # print(52, data)
#         user = await valid_user_statuses(data.sub, statuses, session)
#         return user

async def valid_token(request: Request):
    try:
        # cookie_token = await security.get_access_token_from_request(request)
        data = await security.access_token_required(request)
    except exceptions.MissingTokenError as e:
        raise MissingJWTTokenError(f"Undefined token in cookie")
    except exceptions.JWTDecodeError as e:
        raise JWTDecodeError(f"Invalid token or the access token has expired.")

    return data

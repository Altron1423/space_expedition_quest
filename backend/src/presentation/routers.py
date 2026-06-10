from fastapi import APIRouter

from backend.src.presentation.controllers.example_controller import router as example_router
from backend.src.presentation.controllers.data_base_controller import router as data_base_router
# from backend.src.presentation.controllers._____ import router as ___
#                Тут Ваш файл с контроллером  ^                     ^ Тут название роутера для его идентификации (например example_router2)

api_v1_router = APIRouter()
api_v1_router.include_router(example_router)
api_v1_router.include_router(data_base_router)
# api_v1_router.include_router(example_router2) < добавление Вашего одного роутера к ранее добавленным.

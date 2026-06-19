from fastapi import APIRouter

from backend.src.presentation.controllers.example_controller import router as example_router
from backend.src.presentation.controllers.problem_controller import router as problem_controller
from backend.src.presentation.controllers.team_controller import router as team_controller
from backend.src.presentation.controllers.event_controller import router as event_controller
from backend.src.presentation.controllers.auth_controller import router as auth_controller
from backend.src.presentation.controllers.data_base_controller import router as data_base_router
from backend.src.presentation.controllers.registration_application_controller import router as registration_application_router
# from backend.src.presentation.controllers._____ import router as ___
#                Тут Ваш файл с контроллером  ^                     ^ Тут название роутера для его идентификации (например example_router2)
import backend.src.infrastructures.binders
api_v1_router = APIRouter()
api_v1_router.include_router(example_router)
api_v1_router.include_router(data_base_router)
api_v1_router.include_router(problem_controller)
api_v1_router.include_router(team_controller)
api_v1_router.include_router(event_controller)
api_v1_router.include_router(auth_controller)
api_v1_router.include_router(registration_application_router)
# api_v1_router.include_router(example_router2) < добавление Вашего одного роутера к ранее добавленным.

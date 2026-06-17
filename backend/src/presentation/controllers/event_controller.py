from uuid import UUID, uuid4

from fastapi import APIRouter, Request, Body

from application.use_cases.auth.token_validator import TokenValidatorUseCase, StatusEnum
from backend.src.application.dtos.event import CreateEventDTO
# from backend.src.application.use_cases.auth.token_validator import TokenValidatorUseCase
from backend.src.application.use_cases.events.list_events import GetEventsUseCase
from backend.src.application.use_cases.events.create_event import CreateEventUseCase
from backend.src.presentation.mappers.event import (
    EventsPresentationMapper,
    EventPresentationMapper
)
from backend.src.presentation.schemas.request import (
    CreateEventRequest
)
from backend.src.presentation.schemas.responses import (
    EventResponseSchema,
    EventsResponseSchema
)


router = APIRouter(prefix="/even", tags=["Events"])

@router.get(
    "/get_all",
    response_model=EventsResponseSchema,
    summary="Get all events",
    responses={
        200: {"description": "Events retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Events not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def get_events(
    request: Request,
) -> EventsResponseSchema:
    """
    Возвращает все существующие задачи.
    :param request:
    :return:
    """

    await TokenValidatorUseCase(request)

    events_dto = await GetEventsUseCase()
    return EventsPresentationMapper.to_response(events_dto)


@router.post(
    "/create",
    response_model=EventResponseSchema,
    summary="Create new event",
    responses={
        200: {"description": "Events retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Events not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
async def create_event(
    request: Request,
    body: CreateEventRequest = Body(...),
) -> EventResponseSchema:
    """
    Создание нового продукта.
    """

    await TokenValidatorUseCase(request, StatusEnum.admin)

    event_uuid = uuid4()

    dto = CreateEventDTO(
        unique_id=event_uuid,
        name=body.name,
        description=body.description,
        location=body.location,
        date=body.date,
        problems=body.problems,
    )

    product_dto = await CreateEventUseCase(dto)
    return EventPresentationMapper.to_response(product_dto)




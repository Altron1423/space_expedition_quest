from fastapi import APIRouter, Request
from sqlalchemy import select

from application.use_cases.auth.token_validator import TokenValidatorUseCase, StatusEnum
from backend.src.infrastructures.models.registration_application import (
    RegistrationApplicationModel,
)
from backend.src.infrastructures.uow import UnitOfWorkSQLAlchemy
from backend.src.presentation.schemas.request import RegistrationApplicationRequest
from backend.src.presentation.schemas.responses import (
    RegistrationApplicationResponseSchema,
    RegistrationApplicationsResponseSchema,
)


router = APIRouter(prefix="/registration-applications", tags=["Registration applications"])


async def ensure_registration_application_table(session) -> None:
    await session.run_sync(
        lambda sync_session: RegistrationApplicationModel.__table__.create(
            sync_session.bind,
            checkfirst=True,
        )
    )


@router.post(
    "",
    response_model=RegistrationApplicationResponseSchema,
    summary="Create registration application",
)
async def create_registration_application(
    body: RegistrationApplicationRequest,
) -> RegistrationApplicationResponseSchema:
    async with UnitOfWorkSQLAlchemy() as session:
        await ensure_registration_application_table(session)
        application = RegistrationApplicationModel(
            name=body.name.strip(),
            email=str(body.email),
        )
        session.add(application)
        await session.flush()

        return RegistrationApplicationResponseSchema(
            unique_id=application.unique_id,
            name=application.name,
            email=application.email,
            status=application.status,
            created_at=application.created_at,
        )


@router.get(
    "",
    response_model=RegistrationApplicationsResponseSchema,
    summary="Get registration applications",
)
async def get_registration_applications(
    request: Request,
) -> RegistrationApplicationsResponseSchema:
    await TokenValidatorUseCase(request, StatusEnum.admin)

    async with UnitOfWorkSQLAlchemy() as session:
        await ensure_registration_application_table(session)
        result = await session.execute(
            select(RegistrationApplicationModel).order_by(
                RegistrationApplicationModel.created_at.desc()
            )
        )
        applications = result.scalars().all()

        return RegistrationApplicationsResponseSchema(
            applications=[
                RegistrationApplicationResponseSchema(
                    unique_id=application.unique_id,
                    name=application.name,
                    email=application.email,
                    status=application.status,
                    created_at=application.created_at,
                )
                for application in applications
            ]
        )

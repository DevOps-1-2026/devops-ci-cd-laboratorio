from uuid import uuid4

from .models import (
    ApplicationStatus,
    CreditApplication,
    CreditApplicationCreate,
)


credit_applications: dict[str, CreditApplication] = {}


def create_credit_application(data: CreditApplicationCreate) -> CreditApplication:
    application = CreditApplication(
        application_id=str(uuid4()),
        status=ApplicationStatus.PENDING,
        **data.model_dump(),
    )
    credit_applications[application.application_id] = application
    return application


def list_credit_applications() -> list[CreditApplication]:
    return list(credit_applications.values())


def get_credit_application(application_id: str) -> CreditApplication | None:
    return credit_applications.get(application_id)


def update_credit_application_status(
    application_id: str, status: ApplicationStatus
) -> CreditApplication | None:
    application = get_credit_application(application_id)
    if application is None:
        return None
    application.status = status
    return application

from fastapi import FastAPI, HTTPException

from .models import (
    CreditApplication,
    CreditApplicationCreate,
    CreditApplicationStatusUpdate,
)
from .service import (
    create_credit_application,
    get_credit_application,
    list_credit_applications,
    update_credit_application_status,
)

app = FastAPI(title="DevOps Bank Credit Application API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/credit-applications", response_model=CreditApplication, status_code=201
)
def create_application(data: CreditApplicationCreate):
    return create_credit_application(data)


@app.get("/credit-applications", response_model=list[CreditApplication])
def list_applications():
    return list_credit_applications()


@app.get("/credit-applications/{application_id}", response_model=CreditApplication)
def get_application(application_id: str):
    application = get_credit_application(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Credit application not found")
    return application


@app.put(
    "/credit-applications/{application_id}/status",
    response_model=CreditApplication,
)
def update_application_status(
    application_id: str, data: CreditApplicationStatusUpdate
):
    application = update_credit_application_status(application_id, data.status)
    if application is None:
        raise HTTPException(status_code=404, detail="Credit application not found")
    return application

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_academic_service
from app.schemas import SubscriberCreate, SubscriberRead, SubscriberUpdate
from app.services.academic_service import (
    AcademicService,
    ResourceConflictError,
    ResourceNotFoundError,
)

router = APIRouter(prefix="/subscribers", tags=["Subscribers"])


@router.post("", response_model=SubscriberRead, status_code=status.HTTP_201_CREATED)
def create_subscriber(
    payload: SubscriberCreate,
    service: AcademicService = Depends(get_academic_service),
):
    try:
        return service.create_subscriber(payload)
    except ResourceConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=list[SubscriberRead])
def list_subscribers(service: AcademicService = Depends(get_academic_service)):
    return service.list_subscribers()


@router.get("/{email}", response_model=SubscriberRead)
def get_subscriber(email: str, service: AcademicService = Depends(get_academic_service)):
    try:
        return service.get_subscriber(email)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{email}", response_model=SubscriberRead)
def update_subscriber(
    email: str,
    payload: SubscriberUpdate,
    service: AcademicService = Depends(get_academic_service),
):
    try:
        return service.update_subscriber(email, payload)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(email: str, service: AcademicService = Depends(get_academic_service)):
    try:
        service.delete_subscriber(email)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

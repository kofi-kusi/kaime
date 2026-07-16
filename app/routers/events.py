from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_academic_service
from app.schemas import EventCreate, EventRead, EventUpdate
from app.services.academic_service import (
    AcademicService,
    ResourceConflictError,
    ResourceNotFoundError,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    service: AcademicService = Depends(get_academic_service),
):
    try:
        return service.create_event(payload)
    except ResourceConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=list[EventRead])
def list_events(service: AcademicService = Depends(get_academic_service)):
    return service.list_events()


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, service: AcademicService = Depends(get_academic_service)):
    try:
        return service.get_event(event_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    payload: EventUpdate,
    service: AcademicService = Depends(get_academic_service),
):
    try:
        return service.update_event(event_id, payload)
    except ResourceConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{event_id}/activate", response_model=EventRead)
def activate_event(event_id: int, service: AcademicService = Depends(get_academic_service)):
    try:
        return service.set_event_active(event_id, True)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{event_id}/deactivate", response_model=EventRead)
def deactivate_event(event_id: int, service: AcademicService = Depends(get_academic_service)):
    try:
        return service.set_event_active(event_id, False)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, service: AcademicService = Depends(get_academic_service)):
    try:
        service.delete_event(event_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

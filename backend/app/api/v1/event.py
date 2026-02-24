from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.app.schemas import (
    AllElementsResponseDTO,
    CreateEventDTO,
    CreateEventResponseDTO,
    ManagementEventsProtocol, # -
)
from backend.app.services import get_event_service


router = APIRouter()

@router.get(
    "",
    summary="Список всех валентинок",
    description="ИНФО: Ручка для получения списка всех валентинок.",
    status_code=status.HTTP_200_OK,
)
async def list_events(
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> list[AllElementsResponseDTO]:
    return await service.all_events()

@router.post(
    "",
    summary="Создание валентинки",
    description="ИНФО: Ручка для создания валентинки. Принимает в себя title и text.",
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    data: Annotated[CreateEventDTO, Depends(CreateEventDTO.validate_form)],
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> CreateEventResponseDTO:
    return await service.create_events(data)

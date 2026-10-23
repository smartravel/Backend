from uuid import UUID
from fastapi import APIRouter, Depends, status
from src.api.dependencies import get_current_user_id, get_trip_service
from src.schemas.trip import TripCreateRequest, TripJoinRequest, TripListResponse, TripResponse
from src.services.trip import TripService

router = APIRouter(prefix="/trips", tags=["trips"])

@router.get("", response_model=TripListResponse, status_code=status.HTTP_200_OK)
async def my_trips(
    user_id: UUID = Depends(get_current_user_id),
    service: TripService = Depends(get_trip_service),
):
    return await service.list_my_trips(user_id)

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    payload: TripCreateRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: TripService = Depends(get_trip_service),
):
    return await service.create_trip(
        user_id=user_id,
        title=payload.title,
        destination=payload.destination,
        start_date=payload.start_date,
        end_date=payload.end_date,
        password=payload.password,
    )

@router.post("/join", response_model=TripResponse, status_code=status.HTTP_200_OK)
async def join_trip(
    payload: TripJoinRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: TripService = Depends(get_trip_service),
):
    return await service.join_trip(user_id, payload.invite_token, payload.password)

@router.get("/{trip_id}", response_model=TripResponse, status_code=status.HTTP_200_OK)
async def get_trip(
    trip_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    service: TripService = Depends(get_trip_service),
):
    return await service.get_trip(user_id, trip_id)
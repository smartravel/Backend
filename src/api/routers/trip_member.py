from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies import get_trip_service, require_trip_member
from src.dto.trip_member import TripAccessDTO
from src.schemas.trip import TripMemberResponse
from src.services.trip import TripService

router = APIRouter(
    prefix="/trips/{trip_id}/members",
    tags=["trip members"],
    dependencies=[Depends(require_trip_member)],
)

@router.get("", response_model=list[TripMemberResponse], status_code=status.HTTP_200_OK)
async def list_members(
    trip_id: UUID,
    service: TripService = Depends(get_trip_service),
):
    return await service.list_members(trip_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    user_id: UUID,
    access: TripAccessDTO = Depends(require_trip_member),
    service: TripService = Depends(get_trip_service),
):
    await service.remove_member(access, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
from typing import AsyncIterator, Optional
from uuid import UUID

from fastapi import Cookie, Depends

from src.core.enums import TripRole
from src.core.exceptions import NotTripMember, NotTripOrganizer, TripNotFound, Unauthed
from src.core.security import decode_token
from src.core.uow import get_uow
from src.dto.trip_member import TripAccessDTO
from src.services.auth import AuthService
from src.services.trip import TripService


async def get_auth_service() -> AsyncIterator[AuthService]:
    async with get_uow() as uow:
        yield AuthService(uow)

async def get_trip_service() -> AsyncIterator[TripService]:
    async with get_uow() as uow:
        yield TripService(uow)

async def get_current_user_id(access_token: Optional[str] = Cookie(default=None)) -> UUID:
    if not access_token:
        raise Unauthed
    payload = decode_token(access_token)
    if not payload or payload.get("type") != "access":
        raise Unauthed
    return UUID(payload["sub"])

async def require_trip_member(
    trip_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> TripAccessDTO:
    async with get_uow() as uow:
        if not await uow.trip.get_by_id(trip_id):
            raise TripNotFound
        role = await uow.trip_member.get_role(trip_id, user_id)

    if not role:
        raise NotTripMember

    return TripAccessDTO(trip_id=trip_id, user_id=user_id, role=role)

async def require_organizer(
    access: TripAccessDTO = Depends(require_trip_member),
) -> TripAccessDTO:
    if access.role != TripRole.ORGANIZER:
        raise NotTripOrganizer

    return access
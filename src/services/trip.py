import secrets
from collections import defaultdict
from datetime import date
from uuid import UUID

from src.core.enums import TripRole
from src.core.exceptions import NotTripMember, TooManyAttempts, TripNotFound, WrongTripPassword
from src.core.redis import redis_service
from src.core.security import hash_password, verify_password
from src.core.uow import UnitOfWork
from src.dto.trip import TripCardDTO, TripCountsDTO, TripDetailDTO, TripDTO, TripListDTO
from src.dto.trip_member import TripMemberDTO
from src.utils.dates import days_until, today, trip_status

MAX_JOIN_ATTEMPTS = 5
JOIN_ATTEMPTS_WINDOW = 15 * 60

class TripService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_my_trips(self, user_id: UUID) -> TripListDTO:
        trips = await self.uow.trip.list_for_user(user_id)
        members = await self.uow.trip_member.list_by_trips([trip.id for trip, _ in trips])

        members_by_trip: dict[UUID, list[TripMemberDTO]] = defaultdict(list)
        for member in members:
            members_by_trip[member.trip_id].append(member)

        current = today()
        cards = [
            self._to_card(trip, role, members_by_trip[trip.id], current)
            for trip, role in trips
        ]

        active = sorted((c for c in cards if c.status != "finished"), key=lambda c: c.start_date)
        past = sorted((c for c in cards if c.status == "finished"), key=lambda c: c.start_date, reverse=True)
        counts = TripCountsDTO(all=len(cards), upcoming=len(active), past=len(past))

        return TripListDTO(items=active + past, counts=counts)

    async def create_trip(
        self,
        user_id: UUID,
        title: str,
        destination: str | None,
        start_date: date,
        end_date: date,
        password: str,
    ) -> TripDetailDTO:
        trip = await self.uow.trip.create(
            title=title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            password_hash=await hash_password(password),
            invite_token=secrets.token_urlsafe(16),
            created_by=user_id,
        )
        await self.uow.trip_member.add(trip.id, user_id, TripRole.ORGANIZER)

        return await self._to_detail(trip, TripRole.ORGANIZER)

    async def join_trip(self, user_id: UUID, invite_token: str, password: str) -> TripDetailDTO:
        trip = await self.uow.trip.get_by_invite_token(invite_token)
        if not trip:
            raise TripNotFound

        role = await self.uow.trip_member.get_role(trip.id, user_id)
        if role:
            return await self._to_detail(trip, role)

        attempts_key = f"join_attempts:{trip.id}:{user_id}"
        attempts = await redis_service.get(attempts_key)
        if attempts and int(attempts) >= MAX_JOIN_ATTEMPTS:
            raise TooManyAttempts(retry_after=await redis_service.ttl(attempts_key))

        password_hash = await self.uow.trip.get_password_hash(trip.id)
        if not await verify_password(password, password_hash):
            await redis_service.incr_with_ttl(attempts_key, JOIN_ATTEMPTS_WINDOW)
            raise WrongTripPassword

        await redis_service.delete(attempts_key)
        await self.uow.trip_member.add(trip.id, user_id, TripRole.MEMBER)

        return await self._to_detail(trip, TripRole.MEMBER)

    async def get_trip(self, user_id: UUID, trip_id: UUID) -> TripDetailDTO:
        trip = await self.uow.trip.get_by_id(trip_id)
        if not trip:
            raise TripNotFound

        role = await self.uow.trip_member.get_role(trip_id, user_id)
        if not role:
            raise NotTripMember

        return await self._to_detail(trip, role)

    async def _to_detail(self, trip: TripDTO, role: TripRole) -> TripDetailDTO:
        members = await self.uow.trip_member.list_by_trip(trip.id)
        current = today()

        return TripDetailDTO(
            id=trip.id,
            title=trip.title,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            status=trip_status(trip.start_date, trip.end_date, current),
            days_left=days_until(trip.start_date, current),
            my_role=role,
            invite_token=trip.invite_token,
            members_count=len(members),
            members=members,
        )

    @staticmethod
    def _to_card(trip: TripDTO, role: TripRole, members: list[TripMemberDTO], current: date) -> TripCardDTO:
        return TripCardDTO(
            id=trip.id,
            title=trip.title,
            start_date=trip.start_date,
            end_date=trip.end_date,
            status=trip_status(trip.start_date, trip.end_date, current),
            days_left=days_until(trip.start_date, current),
            my_role=role,
            members_count=len(members),
            members=members,
        )
from uuid import UUID
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

class ConnectionManager:
    def __init__(self):
        self._rooms: dict[UUID, dict[UUID, set[WebSocket]]] = {}

    def connect(self, trip_id: UUID, user_id: UUID, websocket: WebSocket) -> None:
        self._rooms.setdefault(trip_id, {}).setdefault(user_id, set()).add(websocket)

    def disconnect(self, trip_id: UUID, user_id: UUID, websocket: WebSocket) -> None:
        room = self._rooms.get(trip_id)
        if not room:
            return
        sockets = room.get(user_id)
        if sockets:
            sockets.discard(websocket)
            if not sockets:
                room.pop(user_id, None)
        if not room:
            self._rooms.pop(trip_id, None)

    async def broadcast(self, trip_id: UUID, event_type: str, data: dict) -> None:
        message = jsonable_encoder({"type": event_type, "data": data})
        for user_id, sockets in list(self._rooms.get(trip_id, {}).items()):
            for websocket in list(sockets):
                try:
                    await websocket.send_json(message)
                except Exception:
                    self.disconnect(trip_id, user_id, websocket)

    async def kick(self, trip_id: UUID, user_id: UUID) -> None:
        sockets = self._rooms.get(trip_id, {}).get(user_id, set())
        for websocket in list(sockets):
            try:
                await websocket.close(code=4403)
            except Exception:
                pass
            self.disconnect(trip_id, user_id, websocket)

ws_manager = ConnectionManager()
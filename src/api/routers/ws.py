from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from src.core.config import config
from src.core.security import decode_token
from src.core.uow import get_uow
from src.ws.manager import ws_manager

router = APIRouter(tags=["ws"])

@router.websocket("/ws/trips/{trip_id}")
async def trip_ws(websocket: WebSocket, trip_id: UUID):
    origin = websocket.headers.get("origin")
    if origin is not None and origin not in config.cors.origins:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    token = websocket.cookies.get("access_token")
    payload = decode_token(token) if token else None
    if not payload or payload.get("type") != "access":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = UUID(payload["sub"])
    async with get_uow() as uow:
        role = await uow.trip_member.get_role(trip_id, user_id)
    if not role:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    ws_manager.connect(trip_id, user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        ws_manager.disconnect(trip_id, user_id, websocket)
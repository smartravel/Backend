from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import config
from src.core.database import engine
from src.core.redis import redis_client
from src.api.routers.auth import router as auth_router
from src.api.routers.trip import router as trip_router
from src.api.routers.trip_member import router as trip_member_router
from src.api.routers.ws import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()
    await engine.dispose()


app = FastAPI(title="SmartTravel API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(trip_router)
app.include_router(trip_member_router)
app.include_router(ws_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["service"])
async def health():
    return {"status": "ok"}
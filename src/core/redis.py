import json
from typing import Any

import redis.asyncio as redis

from src.core.config import config

redis_client = redis.Redis(
    host=config.redis.host,
    port=config.redis.port,
    password=config.redis.password or None,
    db=config.redis.db,
    decode_responses=True,
)


class RedisService:
    def __init__(self, client=redis_client):
        self.client = client

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        await self.client.set(key, value, ex=ttl)

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) > 0

    # noinspection PyAsyncCall
    async def incr_with_ttl(self, key: str, ttl: int) -> int:
        async with self.client.pipeline(transaction=True) as pipe:
            pipe.incr(key)
            pipe.expire(key, ttl, nx=True)
            count, _ = await pipe.execute()
        return count

    async def ttl(self, key: str) -> int:
        return await self.client.ttl(key)

    async def set_json(self, key: str, value: Any, ttl: int | None = None) -> None:
        await self.client.set(key, json.dumps(value, ensure_ascii=False), ex=ttl)

    async def get_json(self, key: str) -> Any | None:
        raw = await self.client.get(key)
        return json.loads(raw) if raw else None


redis_service = RedisService()
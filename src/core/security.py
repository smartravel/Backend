import asyncio
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from pwdlib import PasswordHash
from src.core.config import config

_hasher = PasswordHash.recommended()
DUMMY_PASSWORD_HASH = _hasher.hash("dummy-password")

async def hash_password(password: str) -> str:
    return await asyncio.to_thread(_hasher.hash, password)

async def verify_password(password: str, password_hash: str) -> bool:
    return await asyncio.to_thread(_hasher.verify, password, password_hash)

def create_access_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt.access_token_expire_minutes)
    payload = {"sub": str(user_id), "type": "access", "exp": expire}
    return jwt.encode(payload, config.jwt.secret_key, algorithm=config.jwt.algorithm)

def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=config.jwt.refresh_token_expire_days)
    payload = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(payload, config.jwt.secret_key, algorithm=config.jwt.algorithm)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            config.jwt.secret_key,
            algorithms=[config.jwt.algorithm],
            options={"require": ["exp", "sub", "type"]},
        )
    except jwt.PyJWTError:
        return None
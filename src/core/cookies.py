from fastapi import Response
from src.core.config import config
REFRESH_COOKIE_PATH = "/auth/refresh"

def set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=config.cookies.secure,
        samesite="lax",
        max_age=config.jwt.access_token_expire_minutes * 60,
        path="/",
    )

def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    set_access_cookie(response, access_token)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=config.cookies.secure,
        samesite="lax",
        max_age=config.jwt.refresh_token_expire_days * 24 * 3600,
        path=REFRESH_COOKIE_PATH,
    )

def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        "access_token", path="/", secure=config.cookies.secure, httponly=True, samesite="lax"
    )
    response.delete_cookie(
        "refresh_token", path=REFRESH_COOKIE_PATH, secure=config.cookies.secure, httponly=True, samesite="lax"
    )
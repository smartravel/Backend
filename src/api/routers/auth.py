from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Response, status

from src.api.dependencies import get_auth_service
from src.core.cookies import set_access_cookie, set_auth_cookies
from src.schemas.auth import StatusResponse, UserLoginRequest, UserRegisterRequest
from src.schemas.user import UserResponse
from src.services.auth import AuthService

router = APIRouter(tags=["auth"])

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(
        email=payload.email,
        password=payload.password,
        nickname=payload.nickname,
        avatar_emoji=payload.avatar_emoji,
    )

@router.post("/auth/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: UserLoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(payload.email, payload.password)
    set_auth_cookies(response, result.access_token, result.refresh_token)
    return result

@router.post("/auth/refresh", response_model=StatusResponse, status_code=status.HTTP_200_OK)
async def refresh(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
):
    access_token = await service.refresh(refresh_token)
    set_access_cookie(response, access_token)
    return StatusResponse(status="session_refreshed")

@router.post("/auth/logout", response_model=StatusResponse, status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    return await service.logout(response)

@router.get("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(
    access_token: Optional[str] = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
):
    return await service.get_profile(access_token)
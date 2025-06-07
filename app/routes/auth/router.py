from fastapi import APIRouter
from app.routes.auth.schema import UserLogin, UserRegister, TokenResponse
from app.routes.auth.controller import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    return await register_user(data)

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    return await login_user(data)

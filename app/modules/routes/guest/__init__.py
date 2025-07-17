from fastapi import APIRouter, Depends
from .web import router as guest_web_router


guest_router = APIRouter()

guest_router.include_router(guest_web_router)

__all__ = [
    'guest_router'
]
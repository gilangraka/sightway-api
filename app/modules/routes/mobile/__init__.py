from .auth import router as auth_router
from .pemantau import router as pemantau_router
from .penyandang import router as penyandang_router
from fastapi import APIRouter, Depends

mobile_router = APIRouter()
mobile_router.include_router(auth_router)
mobile_router.include_router(pemantau_router)
mobile_router.include_router(penyandang_router)

__all__ = ["mobile_router"]
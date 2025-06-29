from fastapi import APIRouter, Depends
from app.middleware import auth_middleware, role_middleware

from .auth import router as auth_router
from .manage_admin import router as manage_admin_router
from .manage_category import router as manage_category_router
from .manage_tag import router as manage_tag_router
from .manage_dashboard import router as manage_dashboard_router
from .manage_pemantau import router as manage_pemantau_router
from .manage_penyandang import router as manage_penyandang_router
from .manage_blindstick import router as manage_blindstick_router

# Router untuk route yang butuh auth + superadmin
dashboard_admin_router = APIRouter(
    dependencies=[
        Depends(auth_middleware),
        Depends(role_middleware(["superadmin", "admin"]))
    ]
)

dashboard_superadmin_router = APIRouter(
    dependencies=[
        Depends(auth_middleware),
        Depends(role_middleware(["superadmin"]))
    ]
)

dashboard_superadmin_router.include_router(manage_admin_router)
dashboard_admin_router.include_router(manage_category_router)
dashboard_admin_router.include_router(manage_tag_router)
dashboard_admin_router.include_router(manage_dashboard_router)
dashboard_admin_router.include_router(manage_pemantau_router)
dashboard_admin_router.include_router(manage_penyandang_router)
dashboard_admin_router.include_router(manage_blindstick_router)

__all__ = [
    "auth_router",
    "dashboard_admin_router",
    "dashboard_superadmin_router"
]

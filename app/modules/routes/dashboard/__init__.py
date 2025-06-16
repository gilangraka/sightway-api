from .auth import router as auth_router
from .manage_admin import router as manage_admin_router
from .manage_category import router as manage_category_router
from .manage_tag import router as manage_tag_router
from .manage_dashboard import router as manage_dashboard_router

__all__ = [
    "auth_router", 
    "manage_user_router",
    "manage_admin_router", 
    "manage_category_router", 
    "manage_tag_router",
    "manage_dashboard_router"
]

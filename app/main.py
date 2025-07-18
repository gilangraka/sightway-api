from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core import TORTOISE_ORM

from app.modules.routes.dashboard import auth_router, dashboard_superadmin_router, dashboard_admin_router
from app.modules.routes.guest import guest_router
from app.modules.routes.mobile import mobile_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/dashboard")
app.include_router(dashboard_superadmin_router, prefix="/dashboard")
app.include_router(dashboard_admin_router, prefix="/dashboard")
app.include_router(guest_router, prefix="/guest")
app.include_router(mobile_router, prefix="/mobile")
    
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
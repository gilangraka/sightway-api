from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core import TORTOISE_ORM

from app.modules.routes.dashboard import auth_router, dashboard_superadmin_router, dashboard_admin_router
import app.modules.routes.mobile as mobile
import app.modules.routes.guest as guest

app = FastAPI()

origins = [
    "http://localhost:3000"
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

mobile_routes = [
    mobile.auth_router
]

guest_routes = [
    guest.guest_web_router
]

for route in mobile_routes:
    app.include_router(route, prefix="/mobile")

for route in guest_routes:
    app.include_router(route, prefix="/guest")
    
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
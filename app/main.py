from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core import TORTOISE_ORM

import app.modules.routes.dashboard as dashboard
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

dashboard_routes = [
    dashboard.auth_router,
    dashboard.manage_admin_router,
    dashboard.manage_pemantau_router,
    dashboard.manage_penyandang_router,
    dashboard.manage_dashboard_router,
    dashboard.manage_category_router,
    dashboard.manage_tag_router,
    dashboard.manage_blindstick_router
]

mobile_routes = [
    mobile.auth_router
]

guest_routes = [
    guest.guest_web_router
]

for route in dashboard_routes:
    app.include_router(route, prefix="/dashboard")

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
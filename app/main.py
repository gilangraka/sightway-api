from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import TORTOISE_ORM

from app.routes.dashboard.manage_tag.router import router as manage_tag_router
from app.routes.dashboard.manage_category.router import router as manage_category_router

app = FastAPI()

app.include_router(manage_tag_router)
app.include_router(manage_category_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

from fastapi import APIRouter, status, Depends
from app.modules.controllers.auth import register
from app.modules.controllers.manage_app_history import index, show, store
from app.modules.schemas.manage_app_history import StoreUpdateSchema

router = APIRouter(prefix="/manage-app-history", tags=["Manage App History"])

@router.get("/")
async def index_handler(page: int = 1, q: str = None):
    return await index(page, q)

@router.get("/{id}")
async def show_handler(id:int):
    return await show(id)

@router.post("/", response_model=StoreUpdateSchema)
async def store_handler(data: StoreUpdateSchema):
    return await store(data)
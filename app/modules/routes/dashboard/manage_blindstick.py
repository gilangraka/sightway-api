from fastapi import APIRouter, status
from typing import Optional
from app.modules.controllers.manage_blindstick import index, show, store, update, destroy
from app.modules.schemas.manage_blindstick import StoreUpdateSchema

router = APIRouter(prefix="/manage-blindstick", tags=["Manage Blindstick"])

@router.get("/")
async def index_handler(page: int = 1, is_used: Optional[bool] = None, q: str = None):
    return await index(page, is_used, q)

@router.get("/{id}")
async def show_handler(id: int, page: int = 1, log_days: int = 7):
    return await show(id, page, log_days)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_handler(request: StoreUpdateSchema):
    return await store(request)

@router.put("/{id}")
async def update_handler(id: int, request: StoreUpdateSchema):
    return await update(id, request)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_handler(id: int):
    return await destroy(id)
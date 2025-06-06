from fastapi import APIRouter, status
from app.routes.dashboard.manage_blindstick.controller import index, show, store, update, destroy
from app.routes.dashboard.manage_blindstick.schema import StoreUpdateSchema
from typing import Optional

router = APIRouter(prefix="/manage-blindstick", tags=["manage-blindstick"])

@router.get("/")
async def get_data(page: int = 1, is_used: Optional[bool] = None):
    return await index(page, q)

@router.get("/{id}")
async def get_data_by_id(id: int, page: int = 1, log_days: int = 7):
    return await show(id, page, log_days)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_data(data: StoreUpdateSchema):
    return await store(data)

@router.put("/{id}")
async def update_data(id: int, data: StoreUpdateSchema):
    return await update(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id: int):
    return await destroy(id)
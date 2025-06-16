from fastapi import APIRouter
from typing import Optional
from app.modules.controllers.manage_pemantau import index, show, last_map

router = APIRouter(prefix="/manage-pemantau", tags=["Manage Pemantau"])

@router.get("/")
async def get_data(page: int = 1, q: Optional[str] = None):
    return await index(page, q)

@router.get("/{id}")
async def get_data_by_id(id: int, page: int = 1):
    return await show(id, page)

@router.get("/{id}/map")
async def get_last_map(id: int):
    return await last_map(id)
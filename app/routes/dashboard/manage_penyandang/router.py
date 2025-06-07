from fastapi import APIRouter
from app.routes.dashboard.manage_penyandang.controller import index, show, last_status_blindstick
from typing import Optional

router = APIRouter(prefix="/manage-pemantau", tags=["manage-pemantau"])

@router.get("/")
async def get_data(page: int = 1, q: Optional[str] = None):
    return await index(page, q)

@router.get("/{id}")
async def get_data_by_id(id: int, page: int = 1):
    return await show(id, page)

@router.get("/{id}/map")
async def get_last_status_blindstick(id: int):
    return await last_status_blindstick(id)
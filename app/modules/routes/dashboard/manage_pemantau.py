from fastapi import APIRouter
from typing import Optional
from app.modules.controllers.manage_pemantau import index, show, last_map

router = APIRouter(prefix="/manage-pemantau", tags=["Manage Pemantau"])

@router.get("/")
async def index_handler(page: int = 1, q: Optional[str] = None):
    return await index(page, q)

@router.get("/{id}")
async def show_handler(id: int, page: int = 1):
    return await show(id, page)

@router.get("/{id}/map")
async def last_map_handler(id: int):
    return await last_map(id)
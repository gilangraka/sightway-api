from fastapi import APIRouter
from typing import Optional
from app.modules.controllers.manage_penyandang import index, show, last_status_blindstick

router = APIRouter(prefix="/manage-penyandang", tags=["Manage Penyandang"])

@router.get("/")
async def index_handler(page: int = 1, q: Optional[str] = None):
    return await index(page, q)

@router.get("/{id}")
async def show_handler(id: int, page: int = 1):
    return await show(id, page)

@router.get("/{id}/map")
async def last_status_blindstick_handler(id: int):
    return await last_status_blindstick(id)
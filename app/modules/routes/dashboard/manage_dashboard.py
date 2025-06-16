from fastapi import APIRouter
from app.modules.controllers.manage_dashboard import index

router = APIRouter(prefix="/manage-dashboard", tags=["Manage Dashboard"])

@router.get("/")
async def index_handler():
    return await index()

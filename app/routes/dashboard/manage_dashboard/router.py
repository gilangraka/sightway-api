from fastapi import APIRouter
from app.routes.dashboard.manage_dashboard.controller import index

router = APIRouter(prefix="/manage-dashboard", tags=["manage-dashboard"])

@router.get("/")
async def get_data():
    return await index()

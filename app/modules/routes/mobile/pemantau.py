from http.client import HTTPException
from typing import Optional
from fastapi import APIRouter, Depends
from app.modules.controllers.auth import login
from app.helpers import decode_access_token
from app.modules.controllers.pemantau import search_penyandang, list_penyandang
from app.middleware import auth_middleware, role, role_middleware

router = APIRouter(prefix="/pemantau", tags=["API Mobile Pemantau"])

@router.get("/search-penyandang")
async def search_penyandang_handler(email: str):
    return await search_penyandang(email=email)

@router.get("/list-penyandang")
async def list_penyandang_handler(user_id: int = Depends(auth_middleware), _= Depends(role_middleware(["pemantau"]))):
    return await list_penyandang(pemantau_id=user_id)
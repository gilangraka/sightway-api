from http.client import HTTPException
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.modules.controllers.auth import login
from app.helpers import decode_access_token
from app.modules.controllers.pemantau import search_penyandang, list_penyandang, add_invitation_penyandang
from app.middleware import auth_middleware, role, role_middleware
from app.models import Pemantau
from app.modules.schemas.add_invitation import AddInvitationSchema
    
router = APIRouter(prefix="/pemantau", tags=["API Mobile Pemantau"])

@router.get("/search-penyandang")
async def search_penyandang_handler(
    email: str = Query(..., min_length=3, max_length=100),
    user_id: int = Depends(auth_middleware),
    _= Depends(role_middleware(["pemantau"]))
):
    pemantau = await Pemantau.get_or_none(user_id=user_id)
    return await search_penyandang(pemantau_id=pemantau.id, email=email)


@router.get("/list-penyandang")
async def list_penyandang_handler(
    user_id: int = Depends(auth_middleware),
    _= Depends(role_middleware(["pemantau"]))
):
    return await list_penyandang(pemantau_id=user_id)

@router.post("/add-invitation-penyandang")
async def add_invitation_penyandang_handler(
    request: AddInvitationSchema,
    user_id: int = Depends(auth_middleware),
    user = Depends(role_middleware(["pemantau"])),
):
    pemantau = await Pemantau.get_or_none(user_id=user_id).first()

    return await add_invitation_penyandang(
        pemantau_id=pemantau.id,
        pemantau_name=user.name,
        penyandang_id=request.penyandang_id,
        status_pemantau=request.status_pemantau,
        detail_status_pemantau=request.detail_status_pemantau
    )
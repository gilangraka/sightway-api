from http.client import HTTPException
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.middleware import auth_middleware, role_middleware
from app.models import Penyandang
from app.modules.controllers.penyandang import accept_invitation, list_pemantau
from app.modules.schemas.add_invitation import AcceptInvitationSchema

router = APIRouter(prefix="/penyandang", tags=["API Mobile Penyandang"])

@router.post("/accept-invitation")
async def add_invitation_penyandang_handler(
    request: AcceptInvitationSchema,
    user_id: int = Depends(auth_middleware),
    _ = Depends(role_middleware(["penyandang"])),  
):
    penyandang = await Penyandang.get_or_none(user_id=user_id)

    return await accept_invitation(
        pemantau_id=request.pemantau_id,
        status_pemantau=request.status_pemantau,
        detail_status_pemantau=request.detail_status_pemantau,
        penyandang_id=penyandang.id,
    )

@router.get("/list-pemantau")
async def list_pemantau_handler(   
    user_id: int = Depends(auth_middleware),
    _ = Depends(role_middleware(["penyandang"])),
    status_filter: Optional[str] = Query(None, description="Filter by status pemantau")
):
    penyandang = await Penyandang.get_or_none(user_id=user_id)
    if not penyandang:
        raise HTTPException(
            status_code=404,
            detail="Penyandang not found"
        )
    
    return await list_pemantau(penyandang_id=penyandang.id, status_filter=status_filter)
from app.models.user import User
from app.models.pemantau import Pemantau
from app.models.log_penyandang_status import LogPenyandangStatus
from app.helpers import paginate, validate_unique, generate_slug
from app.routes.dashboard.manage_pemantau.schema import ManagePemantauSchema
from fastapi import Query, APIRouter, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = User.filter(roles__name = "pemanatau").select_related("roles")
        
        return await paginate(
            queryset=query, 
            q=q,
            page=page, 
            schema=ManagePemantauSchema
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(
    id: int,
    page: int = Query(1, ge=1),
):
    try:
        pemantau = await Pemantau.filter(user_id=id).select_related("user").first()
        if pemantau is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pemantau not found"
            )
        
        penyandang_query = pemantau.penyandang.all()

        total = await penyandang_query.count()
        limit = 10
        offset = (page - 1) * limit

        penyandang = await penyandang_query.order_by("-created_at").offset(offset).limit(limit)

        return {
            "pemantau": pemantau,
            "penyandang": {
                "total": total,
                "page": page,
                "data": penyandang
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


async def get_last_map(id: int):
    try:
        data = await LogPenyandangStatus.filter(penyandang_id=id).order_by("-created_at").first()
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
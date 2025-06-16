from fastapi import Query, HTTPException, status
from typing import Optional
from app.helpers import paginate
from app.modules.schemas.manage_penyandang import ManagePenyandangSchema
from app.models import User, Penyandang, Blindstick, LogBlindstick

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = User.filter(roles__name = "pemanatau").prefetch_related("roles")
        
        return await paginate(
            queryset=query, 
            q=q,
            page=page, 
            schema=ManagePenyandangSchema
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
        penyandang = await Penyandang.filter(user_id=id).prefetch_related("user").first()
        if penyandang is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penyandang not found"
            )
        
        pemantau_query = penyandang.pemantau.all()

        total = await pemantau_query.count()
        limit = 10
        offset = (page - 1) * limit

        pemantau = await pemantau_query.order_by("-created_at").offset(offset).limit(limit)

        return {
            "penyandang": penyandang,
            "pemantau": {
                "total": total,
                "page": page,
                "data": pemantau
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


async def last_status_blindstick(id: int):
    try:
        data = await Blindstick.get_or_none(id=id)
        
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blindstick not found"
            )
        
        latest_status = LogBlindstick.filter(blindstick_id=data.id).order_by("-created_at").limit(3)

        return {
            "blindstick": data,
            "latest_status": latest_status
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
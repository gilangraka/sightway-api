from fastapi import Query, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
from app.models import Blindstick
from app.helpers import paginate, validate_unique
from app.modules.schemas.manage_blindstick import StoreUpdateSchema, ManageBlindstickSchema

async def index(
    page: int = (Query(1, ge=1)),
    is_used: Optional[bool] = (Query(None)),
):
    try:
        query = Blindstick.all()

        if is_used is not None:
            query = query.filter(is_used=is_used)
        
        return await paginate(
            queryset=query, 
            page=page, 
            schema=ManageBlindstickSchema
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(
    id: int,
    page: int = Query(1, ge=1),
    log_days: int = (Query(7, ge=1))
):
    try:
        data = await Blindstick.prefetch_related("log_blindstick").get_or_none(id=id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blindstick not found"
            )
        
        log_query = data.log_blindstick

        if str(log_days) in ['1', '3', '7']:
            cutoff = datetime.utcnow() - timedelta(days=log_days)
            log_query = log_query.filter(created_at__gte=cutoff)

        total = await log_query.count()
        limit = 10
        offset = (page - 1) * limit

        logs = await log_query.order_by("-created_at").offset(offset).limit(limit)

        return {
            "blindstick": data,
            "logs": {
                "total": total,
                "page": page,
                "data": logs
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def store(request: StoreUpdateSchema):
    try:
        await validate_unique(Blindstick, "mac_address", request.mac_address)

        payload = request.model_dump()

        new_blindstick = await Blindstick.create(**payload)
        return new_blindstick

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def update(id: int, request: StoreUpdateSchema):
    try:
        blindstick = await Blindstick.get_or_none(id=id)

        if blindstick is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blindstick not found"
            )

        if request.mac_address != blindstick.mac_address:
            await validate_unique(Blindstick, "mac_address", request.mac_address)

        payload = request.dict()

        blindstick.update_from_dict(payload)
        await blindstick.save()
        
        return blindstick

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def destroy(id: int):
    try:
        blindstick = await Blindstick.get_or_none(id=id)

        if blindstick is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="blindstick not found"
            )
        
        if blindstick.is_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="blindstick is used"
            )

        await blindstick.delete()
        return True

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
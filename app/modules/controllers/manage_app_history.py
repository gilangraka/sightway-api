from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import AppHistory
from app.helpers import paginate, validate_unique
from app.modules.schemas.manage_app_history import StoreUpdateSchema, AppHistorySchema

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = AppHistory.all()
        
        return await paginate(
            queryset=query,
            page=page,
            q=q,
            schema=AppHistorySchema  
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(id: int):
    try:
        data = await AppHistory.get_or_none(id=id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App History not found"
            )
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def store(request: StoreUpdateSchema):
    try:
        await validate_unique(AppHistory, "name", request.name)

        payload = request.model_dump()

        new_app_history = await AppHistory.create(**payload)
        return new_app_history

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
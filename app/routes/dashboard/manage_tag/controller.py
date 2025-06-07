from app.models.m_tag import MTag
from app.helpers import paginate, validate_unique, generate_slug
from app.routes.dashboard.manage_tag.schema import StoreUpdateSchema, TagSchema
from fastapi import Query, HTTPException, status
from typing import Optional

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = MTag.all()
        return await paginate(
            queryset=query, 
            page=page, 
            q=q, 
            schema=TagSchema
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(id: int):
    try:
        data = await MTag.get_or_none(id=id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def store(data: StoreUpdateSchema):
    try:
        await validate_unique(MTag, "name", data.name)

        slug = generate_slug(data.name)
        payload = data.dict()
        payload["slug"] = slug

        new_tag = await MTag.create(**payload)
        return new_tag

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def update(id: int, data: StoreUpdateSchema):
    try:
        tag = await MTag.get_or_none(id=id)

        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        if data.name != tag.name:
            await validate_unique(MTag, "name", data.name)

        slug = generate_slug(data.name)
        payload = data.dict()
        payload["slug"] = slug

        tag.update_from_dict(payload)
        await tag.save()
        
        return tag

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def destroy(id: int):
    try:
        tag = await MTag.get_or_none(id=id)

        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        await tag.delete()
        return True

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
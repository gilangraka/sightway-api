from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import MCategory
from app.helpers import paginate, validate_unique, generate_slug
from app.modules.schemas.manage_category import StoreUpdateSchema, CategorySchema

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = MCategory.all()
        
        return await paginate(
            queryset=query,
            page=page,
            q=q,
            schema=CategorySchema  
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(id: int):
    try:
        data = await MCategory.get_or_none(id=id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def store(request: StoreUpdateSchema):
    try:
        await validate_unique(MCategory, "name", request.name)

        slug = generate_slug(request.name)
        payload = request.model_dump()
        payload["slug"] = slug

        new_category = await MCategory.create(**payload)
        return new_category

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def update(id: int, request: StoreUpdateSchema):
    try:
        category = await MCategory.get_or_none(id=id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        if request.name != category.name:
            await validate_unique(MCategory, "name", request.name)

        slug = generate_slug(request.name)
        payload = request.model_dump()
        payload["slug"] = slug

        category.update_from_dict(payload)
        await category.save()
        
        return category

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

async def destroy(id: int):
    try:
        category = await MCategory.get_or_none(id=id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        await category.delete()
        return True

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
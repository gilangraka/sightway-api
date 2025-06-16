from app.models import User, Role
from app.helpers import paginate, validate_unique, hash_password
from app.modules.schemas.manage_admin import ManageAdminSchema, StoreUpdateSchema
from fastapi import HTTPException, status, Query
from typing import Optional

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = User.filter(roles__name = "admin").prefetch_related("roles")
        return await paginate(
            queryset=query, 
            page=page, 
            q=q, 
            schema=ManageAdminSchema
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     
    
# Store pakai controller auth saja

async def destroy(id: int):
    try:
        user = await User.get_or_none(id=id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        has_admin_role = any(role.name == "admin" for role in await user.roles)
        if not has_admin_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have admin role and cannot be deleted"
            )

        await user.delete()
        return True

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
async def reset_password(id: int):
    try:
        user = await User.get_or_none(id=id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        has_admin_role = any(role.name == "admin" for role in await user.roles)
        if not has_admin_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have admin role and cannot be deleted"
            )

        user.password = hash_password("password")
        await user.save()

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
from app.models.user import User
from app.models.role import Role
from app.helpers import paginate, validate_unique, hash_password
from app.routes.dashboard.manage_category.schema import StoreUpdateSchema
from fastapi import Query, APIRouter, HTTPException, status
from typing import Optional

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = User.filter(roles__name = "admin").select_related("roles")
        return await paginate(
            queryset=query, 
            page=page, 
            q=q, 
            fields=["id", "name", "email"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def store(data: StoreUpdateSchema):
    try:
        await validate_unique(User, "email", data.name)

        payload = data.dict()
        payload["password"] = hash_password(payload["password"])

        new_user = await User.create(**payload)
        
        role = await Role.filter(name="admin").first()
        await new_user.roles.add(role)
        
        return new_user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

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
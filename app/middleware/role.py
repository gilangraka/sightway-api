from fastapi import Depends, HTTPException, status
from app.middleware import auth_middleware
from app.models import User, Role
from typing import Callable

def role_middleware(role_name: str) -> Callable:
    async def dependency(payload: dict = Depends(auth_middleware)):
        user = await User.get(id=int(payload["sub"])).prefetch_related("roles")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not any(role.name == role_name for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {role_name}"
            )
        return user
    return dependency
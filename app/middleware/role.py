from fastapi import Depends, HTTPException, status
from app.middleware import auth_middleware
from app.models import User
from typing import Callable, Sequence

def role_middleware(role_names: Sequence[str]) -> Callable:
    async def dependency(user_id: int = Depends(auth_middleware)):
        user = await User.get(id=user_id).prefetch_related("roles")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not any(role.name in role_names for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role(s): {', '.join(role_names)}"
            )
        return user
    return dependency

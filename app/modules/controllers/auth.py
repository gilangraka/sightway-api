from fastapi import HTTPException, status
from app.models import User, Role
from app.helpers import create_access_token, verify_password, validate_unique
from app.modules.schemas.auth import TokenSchema, LoginSchema, RegisterSchema

def login(required_roles: set[str]):
    async def loginTemplate(request: LoginSchema) -> TokenSchema:
        user = await User.get_or_none(email=request.email)
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not any(role.name in required_roles for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User tidak memiliki salah satu dari role yang dibutuhkan: {', '.join(required_roles)}"
            )

        access_token = create_access_token({"sub": str(user.id)})
        return TokenSchema(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    return loginTemplate

def register(role: str):
    async def registerTemplate(request: RegisterSchema) -> TokenSchema:
        checkRole = Role.get_or_none(name=request.name)
        if checkRole is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {role} tidak tersedia"
            )
        validate_unique(User, "email", request.email)
        if request.password != request.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password dan Konfirmasi password tidak cocok"
            )
        hash_password = hash_password(request.password)
        user = await User.create(name=request.name, email=request.email, password=hash_password)
        user.roles.add(checkRole)

        access_token = create_access_token({"sub": str(user.id)})
        return TokenSchema(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    return registerTemplate
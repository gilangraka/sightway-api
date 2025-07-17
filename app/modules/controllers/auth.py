from fastapi import HTTPException, status
from app.models import User, Role
from app.helpers import create_access_token, verify_password, validate_unique, hash_password
from app.modules.schemas.auth import TokenSchema, LoginSchema, RegisterSchema
from tortoise.contrib.pydantic import pydantic_model_creator

User_Pydantic = pydantic_model_creator(User, name="User", include=("id", "email", "name", "roles"))
Role_Pydantic = pydantic_model_creator(Role, name="Role", include=("id", "name"))

def login(required_roles: set[str]):
    async def loginTemplate(request: LoginSchema) -> TokenSchema:
        user = await User.get_or_none(email=request.email).prefetch_related('roles')

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
        user_pydantic = await User_Pydantic.from_tortoise_orm(user)
        roles_pydantic = [
            await Role_Pydantic.from_tortoise_orm(role)
            for role in user.roles
        ]

        return TokenSchema(
            access_token=access_token,
            token_type="bearer",
            user={
                **user_pydantic.model_dump(),
                "roles": [role.model_dump() for role in roles_pydantic]
            },
        )
    return loginTemplate

def register(role: str):
    async def registerTemplate(request: RegisterSchema) -> TokenSchema:
        checkRole = await Role.get_or_none(name=role)
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
        hashed_password = hash_password(request.password)
        user = await User.create(name=request.name, email=request.email, password=hashed_password)
        await user.roles.add(checkRole)

        if role == "penyandang":
            from app.models import Penyandang
            await Penyandang.create(user_id=user.id)

        elif role == "pemantau":
            from app.models import Pemantau
            await Pemantau.create(user_id=user.id)

        access_token = create_access_token({"sub": str(user.id)})
        user_dict = {
            "id" : user.id,
            "name": user.name,
            "email": user.email
        }
        return TokenSchema(
            access_token=access_token,
            token_type="bearer",
            user=user_dict
        )
    return registerTemplate
from fastapi import HTTPException, status
from app.helpers.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User

async def register_user(data):
    existing = await User.get_or_none(email=data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    user = await User.create(
        email=data.email,
        full_name=data.full_name,
        password=hash_password(data.password),
    )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

async def login_user(data):
    user = await User.get_or_none(email=data.email)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

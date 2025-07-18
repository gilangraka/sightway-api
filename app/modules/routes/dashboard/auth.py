from fastapi import APIRouter, Depends
from app.modules.schemas.auth import TokenSchema
from app.modules.controllers.auth import login

router = APIRouter(prefix="/auth", tags=["Auth Dashboard (Superadmin/Admin)"])

@router.post("/login", response_model=TokenSchema)
async def login_handler(token: TokenSchema = Depends(login({"superadmin", "admin"}))):
    return token
from fastapi import APIRouter, status, Depends
from app.modules.controllers.auth import register
from app.modules.controllers.manage_admin import index, destroy, reset_password
from app.modules.schemas.auth import TokenSchema

router = APIRouter(prefix="/manage-admin", tags=["Manage Admin"])

@router.get("/")
async def index_handler(page: int = 1, q: str = None):
    return await index(page, q)

@router.post("/", response_model=TokenSchema)
async def store_handler(token: TokenSchema = Depends(register("admin"))):
    return token

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_handler(id: int):
    return await destroy(id)

@router.post("/{id}/reset_password", description="Password Baru = password")
async def reset_password_handler(id: int):
    return await reset_password(id)
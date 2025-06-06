from fastapi import APIRouter, status
from app.routes.dashboard.manage_admin.controller import index, store, destroy, reset_password
from app.routes.dashboard.manage_admin.schema import StoreUpdateSchema

router = APIRouter(prefix="/manage-admin", tags=["manage-admin"])

@router.get("/")
async def get_data(page: int = 1, q: str = None):
    return await index(page, q)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_data(data: StoreUpdateSchema):
    return await store(data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id: int):
    return await destroy(id)

@router.post("/reset_password/{id}")
async def reset_password(id: int):
    return await reset_password(id, data)
from fastapi import APIRouter, status
from app.modules.controllers.manage_category import index, show, store, update, destroy
from app.modules.schemas.manage_category import StoreUpdateSchema

router = APIRouter(prefix="/manage-category", tags=["Manage Category"])

@router.get("/")
async def get_data(page: int = 1, q: str = None):
    return await index(page, q)

@router.get("/{id}")
async def get_data_by_id(id: int):
    return await show(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_data(request: StoreUpdateSchema):
    return await store(request)

@router.put("/{id}")
async def update_data(id: int, request: StoreUpdateSchema):
    return await update(id, request)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id: int):
    return await destroy(id)
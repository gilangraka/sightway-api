from fastapi import APIRouter, status
from app.routes.dashboard.manage_tag.controller import index, show, store, update, destroy
from app.routes.dashboard.manage_tag.schema import StoreUpdateSchema

router = APIRouter(prefix="/manage-tag", tags=["manage-tag"])

@router.get("/")
async def get_data(page: int = 1, q: str = None):
    return await index(page, q)

@router.get("/{id}")
async def get_data_by_id(id: int):
    return await show(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_data(data: StoreUpdateSchema):
    return await store(data)

@router.put("/{id}")
async def update_data(id: int, data: StoreUpdateSchema):
    return await update(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id: int):
    return await destroy(id)
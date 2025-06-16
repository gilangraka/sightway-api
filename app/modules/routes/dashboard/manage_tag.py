from fastapi import APIRouter, status
from app.modules.controllers.manage_tag import index, show, store, update, destroy
from app.modules.schemas.manage_tag import StoreUpdateSchema

router = APIRouter(prefix="/manage-tag", tags=["Manage Tag"])

@router.get("/")
async def index_handler(page: int = 1, q: str = None):
    return await index(page, q)

@router.get("/{id}")
async def show_handler(id: int):
    return await show(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_handler(request: StoreUpdateSchema):
    return await store(request)

@router.put("/{id}")
async def update_handler(id: int, request: StoreUpdateSchema):
    return await update(id, request)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_handler(id: int):
    return await destroy(id)
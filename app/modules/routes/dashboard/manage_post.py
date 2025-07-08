from fastapi import APIRouter, status
from app.modules.controllers.manage_post import index, show, destroy, store
from app.modules.schemas.manage_post import StoreUpdateSchema

router = APIRouter(prefix="/manage-post", tags=["Manage Post"])

@router.get("/")
async def index_handler(page: int = 1, q: str = None, order: str = None):
    return await index(page, q, order)

@router.get("/{id}")
async def show_handler(id: int):
    return await show(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store_handler(data: StoreUpdateSchema):
    return await store(data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_handler(id: int):
    return await destroy(id)
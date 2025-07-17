from fastapi import APIRouter, status
from app.modules.controllers.guest_web import last_article, last_app_history, show_article, search_article

router = APIRouter(prefix="/web", tags=["Guest Web"])

@router.get("/last-app-history")
async def get_last_app_history():
    return await last_app_history()

@router.get("/last-article")
async def get_last_article():
    return await last_article()

@router.get("/show-article/{slug}")
async def get_show_article(slug: str):
    return await show_article(slug)

@router.get("/search-article")
async def get_search_article(
    page: int = 1,
    q: str = None,
    category: str = None,
    tags: str = None,
):
    return await search_article(q, category, tags, page)
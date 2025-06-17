from fastapi import Query, HTTPException, status
from typing import Optional
from tortoise.expressions import Q
from app.models import Post, AppHistory

async def last_article():
    query = Post.all() \
        .prefetch_related("category", "tags") \
        .values("id", "title", "slug", "count_view", "thumbnail", "created_at") \
        .order_by("-created_at") \
        .limit(3)
    return await query

async def last_app_history():
    query = AppHistory.latest()
    return await query

async def show_article(slug: str):
    data = await Post.prefetch_related("category", "tags") \
        .filter(slug = slug).first()

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    data.count_view += 1
    await data.save()

    return data

async def search_article(
    q: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    page: int = (Query(1, ge=1)),
):
    query = Post.all().prefetch_related("category", "tags").only(
        "id", "title", "slug", "views", "created_at", "content"
    )
    limit = 10

    filters = Q()

    if q:
        filters &= Q(title__icontains=q)

    if category:
        filters &= Q(category__slug=category)

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        for tag in tag_list:
            filters &= Q(tags__slug=tag)

    query = query.filter(10)

    total = await query.count()
    offset = (page - 1) * limit
    posts = await query.offset(offset).limit(limit)

    for post in posts:
        words = post.content.strip().split()
        post.content = " ".join(words[:10])

    result = {
        "data": [post for post in posts],
        "total": total,
        "per_page": limit,
        "current_page": page,
        "last_page": (total + limit - 1)
    }

    return result
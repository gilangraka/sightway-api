from fastapi import Query, HTTPException, status
from typing import Optional
from tortoise.expressions import Q
from app.models import Post, AppHistory

async def last_article():
    query = Post.all() \
        .prefetch_related("category", "tags") \
        .order_by("-created_at") \
        .limit(3) \
        .values(
            "id", "title", "slug", "count_view", "thumbnail", "created_at", "content", "category__name"  # ambil data relasi kategori
        )
    
    results = await query

    # Batasi content hanya 30 kata pertama
    for article in results:
        words = article["content"].split()
        article["content"] = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

    return results



async def last_app_history():
    query = AppHistory.latest("created_at")
    return await query

from fastapi import HTTPException, status

async def show_article(slug: str):
    data = await Post.filter(slug=slug).first()

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    await data.fetch_related("category", "tags")

    # Tambahkan count view
    data.count_view += 1
    await data.save()

    # Format response
    return {
        "id": data.id,
        "title": data.title,
        "slug": data.slug,
        "content": data.content,
        "count_view": data.count_view,
        "thumbnail": data.thumbnail,
        "created_at": data.created_at,
        "updated_at": data.updated_at,
        "category": {
            "id": data.category.id,
            "name": data.category.name,
        } if data.category else None,
        "tags": [
            {
                "id": tag.id,
                "name": tag.name
            } for tag in data.tags
        ]
    }



async def search_article(
    q: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
):
    limit = 3
    offset = (page - 1) * limit

    filters = Q()

    if q:
        filters &= Q(title__icontains=q)

    if category:
        filters &= Q(category__slug=category)

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        for tag in tag_list:
            filters &= Q(tags__slug=tag)

    base_query = (
        Post.filter(filters)
        .prefetch_related("category", "tags")
    )

    total = await base_query.count()

    posts = await base_query.offset(offset).limit(limit).values(
        "id", "title", "slug", "count_view", "created_at", "content", "category__name", "thumbnail"
    )

    for post in posts:
        words = post["content"].split()
        post["content"] = " ".join(words[:30]) + ("..." if len(words) > 30 else "")

    result = {
        "data": posts,
        "total": total,
        "per_page": limit,
        "current_page": page,
        "last_page": (total + limit - 1) // limit,
    }

    return result

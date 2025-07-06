from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import Post, MTag, MCategory
from app.helpers import paginate, validate_unique, generate_slug
from app.modules.schemas.manage_post import StoreUpdateSchema, ManagePostSchema

async def index(
    page: int = (Query(1, ge=1)),
    q: Optional[str] = Query(None)
):
    try:
        query = Post.all()
        
        return await paginate(
            queryset=query,
            page=page,
            q=q,
            schema=ManagePostSchema  
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     

async def show(slug: str):
    try:
        post = await Post.get_or_none(slug=slug).prefetch_related("category", "tags")

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        tags = await post.tags.all().values("id", "name")
        category = {
            "id": post.category.id,
            "name": post.category.name
        }
        
        data = {
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "content": post.content,
            "thumbnail": post.thumbnail,
            "count_view": post.count_view,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "category": category,
            "tags": tags
        }
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def store(request: StoreUpdateSchema):
    try:
        await validate_unique(Post, "title", request.title)

        # Validasi category
        category_obj = await MCategory.get_or_none(id=request.category)
        if not category_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category dengan id {request.category} tidak ditemukan."
            )

        # Validasi tags
        tags = []
        if request.tags:
            tags = await MTag.filter(id__in=request.tags)
            found_ids = {tag.id for tag in tags}
            missing = [tid for tid in request.tags if tid not in found_ids]
            if missing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tag id tidak ditemukan: {missing}"
                )

        # Buat post
        slug = generate_slug(request.title)
        new_post = await Post.create(
            title=request.title,
            thumbnail=request.thumbnail,
            content=request.content,
            category=category_obj,
            slug=slug
        )

        if tags:
            await new_post.tags.add(*tags)

        # Return data lengkap
        return True


    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


async def destroy(slug: str):
    try:
        post = await Post.get_or_none(slug=slug)

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        await post.delete()
        return True

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
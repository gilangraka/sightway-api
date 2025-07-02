from fastapi import HTTPException, status
from app.models import MTag, Post, MCategory, User, LogUser

async def index():
    try:
        data = {
            'total_posts': await Post.all().count(),
            'total_users': await User.all().count(),
            'total_tags': await MTag.all().count(),
            'total_categories': await MCategory.all().count(),
            'total_logs': await LogUser.all().order_by('-id').limit(5).values()
        }
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     
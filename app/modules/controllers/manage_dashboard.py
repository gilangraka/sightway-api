from fastapi import HTTPException, status
from app.models import MTag, Post, MCategory, User, LogUser

async def index():
    try:
        data = {
            'total_posts': await Post.count(),
            'total_users': await User.count(),
            'total_tags': await MTag.count(),
            'total_categories': await MCategory.count(),
            'total_logs': await LogUser.user.order_by(LogUser.id.desc()).limit(5).get(),
        }
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )     
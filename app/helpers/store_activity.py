from fastapi import Query, HTTPException, status
from app.models import LogUser

def store_log(user:int, log: str) :
    async def store():
        try:
            await LogUser.create(user=user, description=log)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    return store
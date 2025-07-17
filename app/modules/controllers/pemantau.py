from fastapi import Query, HTTPException, status
from typing import Optional
from app.helpers import paginate
from app.modules.schemas.manage_pemantau import ManagePemantauSchema
from app.models import User, Pemantau, LogPenyandangStatus, Penyandang

async def search_penyandang(email: str = Query(None, min_length=3, max_length=100)):
    try:
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email query parameter is required"
            )
        
        queryset = await Penyandang.filter(user__email=email)\
            .select_related("user")\
            .values("id", "user_id", "user__name", "user__email")

        penyandang = queryset[0] if queryset else None

        return {
            "penyandang": penyandang,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
async def list_penyandang(pemantau_id: int):
    try:
        queryset = await Pemantau.filter(user_id=pemantau_id).select_related("penyandang", 'penyandang__user').values('penyandang__id', 'penyandang__user__name', 'penyandang__user__email')
            
        return {
            "data": queryset,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
# async def store_penyandang(
#         penyandang_id: int,
#         status: str,
#         detail_status: Optional[str] = None,
# ):
#     try:
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )
from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import Pemantau, Penyandang, PenyandangPemantau
from app.core.firebase import db
from datetime import datetime

async def accept_invitation(
    pemantau_id: int,
    penyandang_id: int,
    status_pemantau: str,
    detail_status_pemantau: Optional[str] = None
):
    pemantau = await Pemantau.get_or_none(id=pemantau_id)
    if not pemantau:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pemantau not found"
        )
    penyandang = await Penyandang.get_or_none(id=penyandang_id)
    if not penyandang:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Penyandang not found"
        )

    await PenyandangPemantau.create(
        penyandang_id=penyandang.id,
        pemantau_id=pemantau.id,
        status=status_pemantau,
        detail_status=detail_status_pemantau
    )

    return {"message": "Invitation accepted successfully"}


async def list_pemantau(penyandang_id: int, status_filter: Optional[str] = None):
    try:
        query = PenyandangPemantau.filter(penyandang_id=penyandang_id)

        if status_filter:
            query = query.filter(status=status_filter)

        queryset = await query.select_related("pemantau", "pemantau__user").values(
            'pemantau__id',
            'pemantau__user__name',
            'pemantau__user__email'
        )

        filtered = [
            q for q in queryset
            if q["pemantau__id"] is not None and q["pemantau__user__name"] is not None
        ]

        return {
            "data": filtered
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
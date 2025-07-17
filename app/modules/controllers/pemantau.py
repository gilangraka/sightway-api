from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import Pemantau, Penyandang, PenyandangPemantau
from app.core.firebase import db
from datetime import datetime

async def search_penyandang(pemantau_id: int, email: str = Query(None, min_length=3, max_length=100)):
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
        
        # Cek apakah penyandang sudah ditambahkan oleh pemantau
        penyandangPemantau = await PenyandangPemantau.filter(
            penyandang_id=penyandang["id"],
            pemantau_id=pemantau_id
        ).first()

        if penyandangPemantau:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Penyandang sudah ditambahkan oleh pemantau ini"
            )

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
        queryset = await Pemantau.filter(user_id=pemantau_id).select_related("penyandang", "penyandang__user").values(
            'penyandang__id',
            'penyandang__user__name',
            'penyandang__user__email'
        )

        # Hapus entri yang nilai relasinya null
        filtered = [
            q for q in queryset
            if q["penyandang__id"] is not None and q["penyandang__user__name"] is not None
        ]

        return {
            "data": filtered
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
async def add_invitation_penyandang(
        pemantau_id: int,
        pemantau_name: str,
        penyandang_id: int,
        status_pemantau: str,
        detail_status_pemantau: Optional[str] = None,
):
    try:
        # Cek apakah penyandang ada
        penyandang = await Penyandang.get_or_none(id=penyandang_id)
        if not penyandang:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penyandang not found"
            )

        # Simpan data ke Firebase
        now = datetime.utcnow().isoformat() + 'Z'
        data = {
            "pemantau_id": pemantau_id,
            "pemantau_name": pemantau_name,
            "penyandang_id": penyandang.id,
            "status_pemantau": status_pemantau,
            "detail_status_pemantau": detail_status_pemantau,
            "invitation_status": "pending",
            "created_at": now,
        }
        db.reference(f"penyandang/{penyandang.id}/invitations").push().set(data)

        return {"message": "Invitation added successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
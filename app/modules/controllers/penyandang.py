from fastapi import Query, HTTPException, status
from typing import Optional
from app.models import Pemantau, Penyandang, PenyandangPemantau
from app.core.firebase import db
from datetime import datetime
from app.helpers.fcm_service import FCMService

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
            'pemantau__user__id',
            'pemantau__user__name',
            'pemantau__user__email',
            'status',
            'detail_status'
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
    
async def send_emergency_to_pemantau(penyandang_id: int):
    fcm = FCMService("firebase_credential.json", "sightway-9f360")
    try:
        query = PenyandangPemantau.filter(penyandang_id=penyandang_id)

        queryset = await query.select_related("pemantau", "pemantau__user", "penyandang", "penyandang_user").values(
            'pemantau__user__id',
            'penyandang__user__name'
        )

        for record in queryset:
            user_id = record["pemantau__user__id"]
            nama_penyandang = record["penyandang__user__name"]
            ref = db.reference(f"/pemantau/{user_id}")

            data = ref.get()
            
            if data is None:
                continue

            token = data.get("fcm_token")
            if token:
                status_code, result = fcm.send_fcm_message(
                    target_token=token,
                    title="Penyandang terdeteksi darurat!",
                    body=(
                        f"Gawattt! Penyandang yang kamu pantau dengan nama {nama_penyandang} "
                        "terdeteksi darurat!!! Cepat cek dan monitoring sekarang!"
                    ),
                    data={"click_action": "FLUTTER_NOTIFICATION_CLICK"}
                )

                if status_code == 200:
                    saved = fcm.save_notification_to_database(
                        user_id=data.user_id,
                        title=data.title,
                        body=data.body
                    )
                    if not saved:
                        raise HTTPException(status_code=500, detail="Notification sent but failed to save to database.")
                    return {"message": "Notification sent and saved successfully"}
                else:
                    raise HTTPException(status_code=500, detail=result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
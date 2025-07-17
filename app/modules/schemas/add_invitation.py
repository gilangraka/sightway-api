from typing import Optional
from pydantic import BaseModel

class AddInvitationSchema(BaseModel):
    penyandang_id: int
    status_pemantau: str
    detail_status_pemantau: Optional[str] = None

class AcceptInvitationSchema(BaseModel):
    pemantau_id: int
    status_pemantau: str
    detail_status_pemantau: Optional[str] = None
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core import TORTOISE_ORM
from pydantic import BaseModel

from app.modules.routes.dashboard import auth_router, dashboard_superadmin_router, dashboard_admin_router
from app.modules.routes.guest import guest_router
from app.modules.routes.mobile import mobile_router
from app.helpers.fcm_service import FCMService

app = FastAPI()
fcm = FCMService("firebase_credential.json", "sightway-9f360")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/dashboard")
app.include_router(dashboard_superadmin_router, prefix="/dashboard")
app.include_router(dashboard_admin_router, prefix="/dashboard")
app.include_router(guest_router, prefix="/guest")
app.include_router(mobile_router, prefix="/mobile")

class FCMRequest(BaseModel):
    token: str
    title: str
    body: str
    user_id: str

@app.post("/send-fcm/")
def send_fcm(data: FCMRequest):
    status_code, result = fcm.send_fcm_message(
        target_token=data.token,
        title=data.title,
        body=data.body,
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
    
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
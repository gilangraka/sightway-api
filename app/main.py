from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core import TORTOISE_ORM

from app.modules.routes.dashboard import auth_router, dashboard_superadmin_router, dashboard_admin_router
from app.modules.routes.guest import guest_router
from app.modules.routes.mobile import mobile_router
from app.helpers.fcm_service import FCMService

app = FastAPI()

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

fcm = FCMService("service-account.json", "sightway-9f360")

@app.post("/send-fcm/")
def send_fcm(token: str, title: str, body: str):
    status_code, result = fcm.send_fcm_message(
        target_token=token,
        title=title,
        body=body,
        data={"click_action": "FLUTTER_NOTIFICATION_CLICK"}
    )
    if status_code == 200:
        return {"message": "Notification sent successfully"}
    else:
        raise HTTPException(status_code=500, detail=result)
    
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
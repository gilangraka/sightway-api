import firebase_admin
from firebase_admin import credentials, messaging, db
from datetime import datetime

class FCMService:
    def __init__(self, credential_path, project_id):
        if not firebase_admin._apps:
            cred = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
                'databaseURL': f"https://{project_id}.firebaseio.com"
            })

    def send_fcm_message(self, target_token: str, title: str, body: str, data: dict):
        message = messaging.Message(
            token=target_token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data,
        )
        try:
            response = messaging.send(message)
            return 200, response
        except Exception as e:
            return 500, str(e)

    def save_notification_to_database(self, user_id: str, title: str, body: str):
        try:
            ref = db.reference(f"push_notifications/{user_id}")
            ref.push({
                "title": title,
                "body": body,
                "created_at": datetime.now().isoformat()
            })
            return True
        except Exception as e:
            print("DB error:", e)
            return False

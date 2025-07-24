import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

class FCMService:
    def __init__(self, service_account_path: str, project_id: str):
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )

    def get_access_token(self):
        auth_req = Request()
        self.credentials.refresh(auth_req)
        return self.credentials.token

    def send_fcm_message(self, target_token: str, title: str, body: str, data: dict = {}):
        url = f"https://fcm.googleapis.com/v1/projects/{self.project_id}/messages:send"
        access_token = self.get_access_token()

        message = {
            "message": {
                "token": target_token,
                "notification": {
                    "title": title,
                    "body": body
                },
                "data": data
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=message)
        return response.status_code, response.json()

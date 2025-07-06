from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import AppHistory

AppHistorySchema = pydantic_model_creator(AppHistory, name="CategorySchema", include=("id", "name", "description", "file_apk", "file_ipa"))

class StoreUpdateSchema(BaseModel):
    name: str
    description: str
    file_apk: str
    file_ipa: str
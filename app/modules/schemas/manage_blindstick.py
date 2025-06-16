from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.blindstick import Blindstick

ManageBlindstickSchema = pydantic_model_creator(Blindstick, name="ManageBlindstickSchema", include=("id", "mac_address", "is_used"))

class StoreUpdateSchema(BaseModel):
    mac_address: str
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import MTag

TagSchema = pydantic_model_creator(MTag, name="TagSchema", include=("id", "name", "slug"))

class StoreUpdateSchema(BaseModel):
    name: str
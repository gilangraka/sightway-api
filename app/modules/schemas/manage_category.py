from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.m_category import MCategory

CategorySchema = pydantic_model_creator(MCategory, name="CategorySchema", include=("id", "name", "slug"))

class StoreUpdateSchema(BaseModel):
    name: str
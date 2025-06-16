from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import User

ManageAdminSchema = pydantic_model_creator(User, name="ManageAdminSchema", include=("id", "name", "email"))

class StoreUpdateSchema(BaseModel):
    name: str
    email: str
    password: str
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.user import User

ManagePenyandangSchema = pydantic_model_creator(User, name="ManagePenyandangSchema", include=("id", "name", "email"))
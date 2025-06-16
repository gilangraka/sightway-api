from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import User

ManagePemantauSchema = pydantic_model_creator(User, name="ManagePemantauSchema", include=("id", "name", "email"))
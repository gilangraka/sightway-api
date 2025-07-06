from pydantic import BaseModel
from typing import List
from app.models import Post
from tortoise.contrib.pydantic import pydantic_model_creator

ManagePostSchema = pydantic_model_creator(Post, name="ManagePostSchema", include=("id", "title", "slug", "thumbnail"))

class StoreUpdateSchema(BaseModel):
    title: str
    thumbnail: str
    content: str
    category: int
    tags: List[int]
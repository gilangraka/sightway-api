from pydantic import BaseModel

class MTagPydantic(BaseModel):
    id: int
    name: str
    slug: str

class StoreUpdateSchema(BaseModel):
    name: str
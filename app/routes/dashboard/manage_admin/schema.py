from pydantic import BaseModel

class StoreUpdateSchema(BaseModel):
    name: str
    email: str
    password: str
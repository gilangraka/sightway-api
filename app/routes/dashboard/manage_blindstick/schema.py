from pydantic import BaseModel

class StoreUpdateSchema(BaseModel):
    mac_address: str
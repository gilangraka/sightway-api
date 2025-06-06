from fastapi import HTTPException
from tortoise.models import Model

async def validate_unique(model: type[Model], field_name: str, value: str | int):
    filter_kwargs = {field_name: value}
    exists = await model.filter(**filter_kwargs).exists()
    if exists:
        model_name = model.__name__
        raise HTTPException(status_code=400, detail=f"{model_name} already exists")

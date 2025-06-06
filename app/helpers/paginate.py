from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationResult(BaseModel, Generic[T]):
    total: int
    page: int
    data: List[T]

async def paginate(queryset, page: int = 1) -> PaginationResult:
    limit = 10  # fixed statis 10
    offset = (page - 1) * limit
    total = await queryset.count()
    data = await queryset.offset(offset).limit(limit)
    return PaginationResult(total=total, page=page, data=data)

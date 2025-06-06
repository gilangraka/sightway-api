from typing import Generic, List, TypeVar
from pydantic import BaseModel
from typing import Optional

T = TypeVar("T")

class PaginationResult(BaseModel, Generic[T]):
    total: int
    page: int
    data: List[T]

async def paginate(
    queryset, 
    page: int = 1, 
    q: Optional[str] = None,
    fields: Optional[list] = None,
) -> PaginationResult:
    limit = 10
    offset = (page - 1) * limit

    if q:
        queryset = queryset.filter(name__icontains=q)

    total = await queryset.count()

    # Paginasi sebelum values supaya tetap QuerySet
    queryset = queryset.offset(offset).limit(limit)

    if fields:
        queryset = queryset.values(*fields)

    data = await queryset
    return PaginationResult(total=total, page=page, data=data)

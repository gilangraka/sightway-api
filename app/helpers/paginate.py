from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from tortoise.models import Model
import math

T = TypeVar("T")

class PaginationResult(BaseModel, Generic[T]):
    total: int
    page: int
    per_page: int
    last_page: int
    data: List[T]

async def paginate(
    queryset,
    page: int = 1,
    q: Optional[str] = None,
    search_field: Optional[str] = "name",
    schema: Optional[BaseModel] = None,
    prefetch: Optional[List[str]] = None,
    limit: int = 10,
    order: str = "desc", 
) -> PaginationResult:
    offset = (page - 1) * limit

    # Apply search filter if q is provided
    if q and search_field:
        filter_expr = {f"{search_field}__icontains": q}
        queryset = queryset.filter(**filter_expr)

    # Apply prefetch_related if needed
    if prefetch:
        queryset = queryset.prefetch_related(*prefetch)

    # Apply order_by
    # Apply order_by
    if order == "asc":
        queryset = queryset.order_by("id")
    else:
        queryset = queryset.order_by("-id")

    total = await queryset.count()
    last_page = math.ceil(total / limit)

    # Apply pagination
    queryset = queryset.offset(offset).limit(limit)

    # Serialize using Pydantic model
    if schema:
        data = await schema.from_queryset(queryset)
    else:
        data = await queryset

    return PaginationResult(
        total=total,
        page=page,
        per_page=limit,
        last_page=last_page,
        data=data,
    )

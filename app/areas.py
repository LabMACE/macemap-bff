from typing import Union, Any
from fastapi import Depends, APIRouter, Query, Response
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID

router = APIRouter()


# @router.get("/{area_id}")
# async def get_area(
#     client: httpx.AsyncClient = Depends(get_async_client),
#     *,
#     area_id: UUID,
#     sort: list[str] | None = None,
#     range: list[int] | None = None,
#     filter: dict[str, str] | None = None,
# ) -> Any:
#     res = await client.get(
#         f"{config.SOIL_API_URL}/v1/areas/{area_id}",
#         params={"sort": sort, "range": range, "filter": filter},
#     )

#     return res.json()


@router.get("")
async def get_areas(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    response: Response,
    sort: list[str] | None = None,
    range: list[int] | None = None,
    filter: dict[str, str] | None = None,
) -> Any:
    # Fetch data from config.SOIL_API_URL/v1/areas/ and relay back to client
    res = await client.get(
        f"{config.SOIL_API_URL}/v1/areas",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]
    return res.json()

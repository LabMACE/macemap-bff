from typing import Any
from fastapi import Depends, APIRouter, Response, Body, Request
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin

router = APIRouter()


@router.get("/{subsite_id}")
async def get_subsite(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    subsite_id: UUID,
) -> Any:
    """Get a subsite by id"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/subsites/{subsite_id}",
    )

    return res.json()


@router.get("")
async def get_subsites(
    request: Request,
    response: Response,
    *,
    filter: str = None,
    sort: str = None,
    range: str = None,
    client: httpx.AsyncClient = Depends(get_async_client),
) -> Any:
    """Get all subsites"""
    res = await client.get(
        f"{config.MACE_API_URL}/v1/subsites",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_subsite(
    subsite: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a subsite"""
    print(user)
    res = await client.post(
        f"{config.MACE_API_URL}/v1/subsites",
        json=subsite,
    )

    return res.json()


@router.put("/{subsite_id}")
async def update_subsite(
    subsite_id: UUID,
    subsite: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """ "Updates a subsite by id"""

    res = await client.put(
        f"{config.MACE_API_URL}/v1/subsites/{subsite_id}", json=subsite
    )

    return res.json()


@router.delete("/{subsite_id}")
async def delete_subsite(
    subsite_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete an subsite by id"""

    res = await client.delete(
        f"{config.MACE_API_URL}/v1/subsites/{subsite_id}"
    )

    return res.json()

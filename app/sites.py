from typing import Any
from fastapi import Depends, APIRouter, Response, Body, Request
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin

router = APIRouter()


@router.get("/{site_id}")
async def get_site(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    site_id: UUID,
) -> Any:
    """Get a site by id"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/sites/{site_id}",
    )

    return res.json()


@router.get("")
async def get_sites(
    request: Request,
    response: Response,
    *,
    filter: str = None,
    sort: str = None,
    range: str = None,
    client: httpx.AsyncClient = Depends(get_async_client),
) -> Any:
    """Get all sites"""
    res = await client.get(
        f"{config.MACE_API_URL}/v1/sites",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_site(
    site: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a site"""

    res = await client.post(
        f"{config.MACE_API_URL}/v1/sites",
        json=site,
    )

    return res.json()


@router.put("/{site_id}")
async def update_site(
    site_id: UUID,
    site: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """ "Updates a site by id"""

    res = await client.put(
        f"{config.MACE_API_URL}/v1/sites/{site_id}", json=site
    )

    return res.json()


@router.delete("/{site_id}")
async def delete_site(
    site_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete an site by id"""

    res = await client.delete(f"{config.MACE_API_URL}/v1/sites/{site_id}")

    return res.json()

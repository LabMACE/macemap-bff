from typing import Any
from fastapi import Depends, APIRouter, Query, Response, Body
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin

router = APIRouter()


@router.get("/{field_campaign_id}")
async def get_field_campaign(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    field_campaign_id: UUID,
) -> Any:
    """Get a field_campaign by id"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/fieldcampaigns/{field_campaign_id}",
    )

    return res.json()


@router.get("")
async def get_field_campaigns(
    response: Response,
    *,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    client: httpx.AsyncClient = Depends(get_async_client),
) -> Any:
    """Get all field_campaigns"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/fieldcampaigns",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    return res.json()


@router.post("")
async def create_field_campaign(
    field_campaign: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates an field_campaign"""

    res = await client.post(
        f"{config.MACE_API_URL}/v1/fieldcampaigns",
        json=field_campaign,
    )

    return res.json()


@router.post("")
async def create_many_field_campaigns(
    field_campaign: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a field_campaign"""

    res = await client.post(
        f"{config.MACE_API_URL}/v1/fieldcampaigns/many",
        json=field_campaign,
    )

    return res.json()


@router.put("/{field_campaign_id}")
async def update_field_campaign(
    field_campaign_id: UUID,
    field_campaign: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Updates a field_campaign by id"""

    res = await client.put(
        f"{config.MACE_API_URL}/v1/fieldcampaigns/{field_campaign_id}",
        json=field_campaign,
    )

    return res.json()


@router.delete("/{field_campaign_id}")
async def delete_field_campaign(
    field_campaign_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete a field_campaign by id"""

    res = await client.delete(
        f"{config.MACE_API_URL}/v1/fieldcampaigns/{field_campaign_id}"
    )

    return res.json()

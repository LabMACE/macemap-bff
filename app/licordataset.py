from typing import Any
from fastapi import Depends, APIRouter, Response, Body, Request
from fastapi.responses import StreamingResponse
from app.config import config
from app.utils import get_async_client
import httpx
from uuid import UUID
from app.models.user import User
from app.auth import require_admin
import orjson

router = APIRouter()


@router.get("/{licordataset_id}")
async def get_licor(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    licordataset_id: str,
) -> Any:
    """Get a licor by id

    The dataset ID is a combination of the licor ID (UUID) and dataset key
    (string) separated by a colon. For example:

        8d4d5f0e-4b6a-4f1b-9e3f-4f7d7c2c2e8e.dataset1

    """

    licor_id, dataset_id = str(licordataset_id).split(".")

    res = await client.get(
        f"{config.MACE_API_URL}/v1/licor/{licor_id}/dataset/{dataset_id}",
    )
    data = res.json()
    data["id"] = licordataset_id
    data["licor_id"] = licor_id

    return data

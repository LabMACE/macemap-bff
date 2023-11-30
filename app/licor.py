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


@router.get("/{licor_id}")
async def get_licor(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    licor_id: UUID,
) -> Any:
    """Get a licor by id"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/licor/{licor_id}",
    )
    data = res.json()

    # Add the url value to each licor to display in the data grid
    data["url"] = f"{config.API_PREFIX}/licor/{data['id']}/download"

    return data


@router.get("/{licor_id}/download")
async def get_licor_data_as_file(
    client: httpx.AsyncClient = Depends(get_async_client),
    *,
    licor_id: UUID,
) -> Any:
    """Get a licor record by id and return as .json file"""

    res = await client.get(
        f"{config.MACE_API_URL}/v1/licor/{licor_id}/data",
    )

    data = res.json()

    encoded_data = orjson.dumps(data)

    return StreamingResponse(
        content=iter([encoded_data]),
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="{name}.json"'.format(
                name=data["name"]
            )
        },
    )


@router.get("")
async def get_licor_all(
    request: Request,
    response: Response,
    *,
    filter: str = None,
    sort: str = None,
    range: str = None,
    client: httpx.AsyncClient = Depends(get_async_client),
) -> Any:
    """Get all licor"""
    res = await client.get(
        f"{config.MACE_API_URL}/v1/licor",
        params={"sort": sort, "range": range, "filter": filter},
    )
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = res.headers["Content-Range"]

    # Add the url value to each licor to display in the data grid
    all_licor = []
    for licor in res.json():
        licor["url"] = f"{config.API_PREFIX}/licor/{licor['id']}/download"
        all_licor.append(licor)

    return all_licor


@router.post("")
async def create_licor(
    licor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """Creates a licor"""
    print(user)
    res = await client.post(
        f"{config.MACE_API_URL}/v1/licor",
        json=licor,
    )

    return res.json()


@router.put("/{licor_id}")
async def update_licor(
    licor_id: UUID,
    licor: Any = Body(...),
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> Any:
    """ "Updates a licor by id"""

    res = await client.put(
        f"{config.MACE_API_URL}/v1/licor/{licor_id}", json=licor
    )

    return res.json()


@router.delete("/{licor_id}")
async def delete_licor(
    licor_id: UUID,
    client: httpx.AsyncClient = Depends(get_async_client),
    user: User = Depends(require_admin),
) -> None:
    """Delete an licor by id"""

    res = await client.delete(f"{config.MACE_API_URL}/v1/licor/{licor_id}")

    return res.json()

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from app.models.config import KeycloakConfig
from app.models.health import HealthCheck
from app.utils import get_async_client
import httpx
from app.sites import router as sites_router
from app.subsites import router as subsites_router
from app.licor import router as licor_router
from app.licordataset import router as licordataset_router
from app.fieldcampaigns import router as field_campaigns_router

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{config.API_PREFIX}/config/keycloak")
async def get_keycloak_config() -> KeycloakConfig:
    return KeycloakConfig(
        clientId=config.KEYCLOAK_CLIENT_ID,
        realm=config.KEYCLOAK_REALM,
        url=config.KEYCLOAK_URL,
    )


@app.get(
    "/healthz",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def get_health(
    client: httpx.AsyncClient = Depends(get_async_client),
) -> HealthCheck:
    """Perform a Health Check

    Useful for Kubernetes to check liveness and readiness probes
    """

    res = await client.get(f"{config.MACE_API_URL}/healthz")
    res_json = res.json()

    if res_json["status"] != "OK":
        raise HTTPException(status_code=500)

    return HealthCheck(status="OK")


app.include_router(
    sites_router,
    prefix=f"{config.API_PREFIX}/sites",
    tags=["sites"],
)
app.include_router(
    subsites_router,
    prefix=f"{config.API_PREFIX}/subsites",
    tags=["subsites"],
)
app.include_router(
    field_campaigns_router,
    prefix=f"{config.API_PREFIX}/fieldcampaigns",
    tags=["fieldcampaigns"],
)
app.include_router(
    licor_router,
    prefix=f"{config.API_PREFIX}/licor",
    tags=["LICOR"],
)
app.include_router(
    licordataset_router,
    prefix=f"{config.API_PREFIX}/licordataset",
    tags=["LICOR", "Dataset"],
)

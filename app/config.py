from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    API_PREFIX: str = "/api"

    # Keycloak settings
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_REALM: str
    KEYCLOAK_URL: str

    # MACE-API settings
    MACE_API_URL: str  # Full path to the MACE API (eg: http://mace-api-dev)


@lru_cache()
def get_config():
    return Config()


config = get_config()

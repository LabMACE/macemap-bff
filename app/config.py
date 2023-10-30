from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_REALM: str
    KEYCLOAK_URL: str


@lru_cache()
def get_config():
    return Config()


config = get_config()

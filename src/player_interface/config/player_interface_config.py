from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class PlayerInterfaceBaseConfig(BaseSettings):
    app_name: str = "Player Interface Service"
    debug: bool = True
    profile: str = "local"
    version: str
    log_level: str = "info"
    cache_host: str = "localhost"
    cache_port: int = 6379
    cache_ttl: int
    cache_timeout: int
    cache_connect_timeout: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return PlayerInterfaceBaseConfig()

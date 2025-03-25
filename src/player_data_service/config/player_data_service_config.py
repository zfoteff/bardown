from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class PlayerDataServiceBaseConfig(BaseSettings):
    app_name: str = "Player Data Service"
    debug: bool = True
    profile: str = "local"
    mysql_host: str = "localhost"
    mysql_user: str
    mysql_password: str
    mysql_root_password: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return PlayerDataServiceBaseConfig()

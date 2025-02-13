from typing import Dict
from src.games import GAMES_TABLE_NAME
from src.players import COACHES_TABLE_NAME, PLAYERS_TABLE_NAME, TEAMS_TABLE_NAME
from src.stats import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME

class DatabaseConfig:
    _config: Dict[str, str] = {}

    PLAYER_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": PLAYERS_TABLE_NAME,
    }
    TEAMS_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": TEAMS_TABLE_NAME,
    }
    COACHES_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": COACHES_TABLE_NAME,
    }
    STATISTICS_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": GAME_STATISTICS_TABLE_NAME,
    }
    SEASON_STATISTICS_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": SEASON_STATISTICS_TABLE_NAME,
    }
    GAMES_TABLE_DB_CONFIG = {
        "user": _config["MYSQL_USER"],
        "password": _config["MYSQL_PASSWORD"],
        "host": _config["MYSQL_HOST"],
        "table": GAMES_TABLE_NAME,
    }

    def __init__(cls, config: Dict[str, str] = {}):
       cls._config = config


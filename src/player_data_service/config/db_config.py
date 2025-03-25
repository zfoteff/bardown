from typing import Dict, Self

from games import GAMES_TABLE_NAME
from players import COACHES_TABLE_NAME, PLAYERS_TABLE_NAME, TEAMS_TABLE_NAME
from stats import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME


class DatabaseConfig:
    user: str
    password: str
    host: str
    PLAYER_TABLE_DB: str
    TEAMS_TABLE_DB: str
    COACHES_TABLE_DB: str
    STATISTICS_TABLE_DB: str
    SEASON_STATISTICS_TABLE_DB: str
    GAMES_TABLE_DB: str

    def __init__(self, table: str) -> Self:
        from os import environ

        self.user = environ["MYSQL_USER"]
        self.password = environ["MYSQL_PASSWORD"]
        self.host = environ["MYSQL_HOST"]
        self.table = table

    def _to_dict(self) -> Dict[str, str]:
        return {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "table": self.table,
        }


def get_player_table_db() -> DatabaseConfig:
    return DatabaseConfig(PLAYERS_TABLE_NAME)


def get_teams_table_db() -> dict:
    return DatabaseConfig(TEAMS_TABLE_NAME)


def get_coaches_table_db() -> dict:
    return DatabaseConfig(COACHES_TABLE_NAME)


def get_statistics_table_db() -> dict:
    return DatabaseConfig(GAME_STATISTICS_TABLE_NAME)


def get_season_statistics_table_db() -> dict:
    return DatabaseConfig(SEASON_STATISTICS_TABLE_NAME)


def get_games_table_db() -> dict:
    return DatabaseConfig(GAMES_TABLE_NAME)

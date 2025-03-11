from typing import Dict
from games import GAMES_TABLE_NAME
from players import COACHES_TABLE_NAME, PLAYERS_TABLE_NAME, TEAMS_TABLE_NAME
from stats import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME

class DatabaseConfig:
    def __init__(self, config: Dict[str, str] = {}):
        self.PLAYER_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": PLAYERS_TABLE_NAME,
        }
        self.TEAMS_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": TEAMS_TABLE_NAME,
        }
        self.COACHES_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": COACHES_TABLE_NAME,
        }
        self.STATISTICS_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": GAME_STATISTICS_TABLE_NAME,
        }
        self.SEASON_STATISTICS_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": SEASON_STATISTICS_TABLE_NAME,
        }
        self.GAMES_TABLE_DB = {
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "host": config["MYSQL_HOST"],
            "table": GAMES_TABLE_NAME,
        }
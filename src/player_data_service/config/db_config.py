import os

from dotenv import load_dotenv
from players import COACHES_TABLE_NAME, PLAYERS_TABLE_NAME, TEAMS_TABLE_NAME
from games import GAMES_TABLE_NAME
from stats.__init___ import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME

load_dotenv()


PLAYER_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": PLAYERS_TABLE_NAME,
}
TEAMS_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": TEAMS_TABLE_NAME,
}
COACHES_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": COACHES_TABLE_NAME,
}
STATISTICS_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": GAME_STATISTICS_TABLE_NAME,
}
SEASON_STATISTICS_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": SEASON_STATISTICS_TABLE_NAME,
}
GAMES_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": GAMES_TABLE_NAME,
}
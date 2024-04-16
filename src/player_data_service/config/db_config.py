import os

from dotenv import load_dotenv

load_dotenv()


PLAYER_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": "players",
}

STATISTICS_TABLE_DB_CONFIG = {
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "host": os.environ["MYSQL_HOST"],
    "table": "players",
}

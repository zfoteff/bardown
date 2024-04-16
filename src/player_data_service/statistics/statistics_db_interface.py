__version__ = "1.0.0"
__author__ = "Zac Foteff"

from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from src.logger import Logger
from src.player_data_service.config.db_config import STATISTICS_TABLE_DB_CONFIG
from src.player_data_service.db_client import MySQLClient
from src.player_data_service.statistics import TABLE_NAME

logger = Logger("player-db-interface")


class PlayerDatabaseInterface:
    def __init__(self):
        self.__client = MySQLClient(**STATISTICS_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def close_connection(self):
        self.__client.close_connection()

    def create_game_statistics(self):
        pass

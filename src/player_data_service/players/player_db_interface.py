__version__ = "1.0.0"
__author__ = "Zac Foteff"

import re

from player_data_service.db_client import MySQLClient as client
from src.logger import Logger

logger = Logger("player-db-interface")


class PlayerDatabaseInterface:
    def __init__(self):
        self.__client = client({})
        self.__client.open_connection()

    def close_connection(self):
        self.__client.close_connection()

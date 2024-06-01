from bin.logger import Logger
from connectors.mysql import MySQLClient

from config.db_config import GAMES_TABLE_DB_CONFIG 
logger = Logger("db")

class GamesDBInterface:
    def __init__(self):
        self.__client = MySQLClient(**GAMES_TABLE_DB_CONFIG)
        self.__client.open_connection()
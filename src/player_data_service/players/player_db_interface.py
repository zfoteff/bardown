__version__ = "1.0.0"
__author__ = "Zac Foteff"

from typing import List, Tuple

from src.logger import Logger
from src.player_data_service.config.db_config import PLAYER_TABLE_DB_CONFIG
from src.player_data_service.db_client import MySQLClient
from src.player_data_service.players.models.dto.player import Player

logger = Logger("player-db-interface")


class PlayerDatabaseInterface:
    def __init__(self):
        self.__client = MySQLClient(**PLAYER_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def close_connection(self):
        self.__client.close_connection()

    def create_player(self, player: Player) -> bool:
        query = f""

    def get_players(
        self, limit: int = None, offset: int = None, order: str = None
    ) -> Tuple[bool, List]:
        query = f"SELECT * FROM players"

        if order is not None:
            (direction, field) = order
            query += f" ORDER BY {field} {direction}"

        if limit is not None:
            query += f" LIMIT {limit}"

        if offset is not None:
            query += f" OFFSET {offset}"

        success, result = self.__client.execute_query(query)

        if not success:
            return False, []

        logger.info(result)
        return True, result

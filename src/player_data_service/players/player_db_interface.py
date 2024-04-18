__version__ = "1.0.0"
__author__ = "Zac Foteff"

from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from src.logger import Logger
from src.player_data_service.config.db_config import PLAYER_TABLE_DB_CONFIG
from src.player_data_service.db_client import MySQLClient
from src.player_data_service.errors.player_validation_error import (
    PlayerAlreadyExists,
    PlayerDoesNotExist,
)
from src.player_data_service.players import TABLE_NAME
from src.player_data_service.players.models.dao.player import Player as PlayerDAO
from src.player_data_service.players.models.dto.player import Player as PlayerDTO
from src.player_data_service.players.models.dto.players_request_filters import (
    PlayersRequestFilters,
)

logger = Logger("player-db-interface")


class PlayerDatabaseInterface:
    def __init__(self):
        self.__client = MySQLClient(**PLAYER_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def close_connection(self):
        self.__client.close_connection()

    def _build_query_from_filters(self, filters: PlayersRequestFilters) -> str:
        query = f"SELECT * FROM players"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def create_player(self, player: PlayerDTO) -> bool | PlayerAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_player_id = str(uuid4())
        query = f"""
            INSERT INTO players 
            VALUES (
                "{new_player_id}",
                {player.number},
                "{player.first_name}", 
                "{player.last_name}", 
                "{player.position}", 
                "{player.grade}", 
                "{player.school}", 
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False, ""

        player.player_id = new_player_id
        player.created = create_modify_time
        player.modified = create_modify_time
        return True

    def update_player(
        self, player_id: str, player: PlayerDTO
    ) -> str | PlayerDoesNotExist:
        player_id = self.player_exists(player_id)
        query = f"""
            UPDATE f{TABLE_NAME}
            SET number={player.number},
                first_name="{player.first_name}",
                last_name="{player.last_name}",
                position="{player.position}",
                grade="{player.grade}",
                school="{player.school}",
                modified="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
            WHERE player_id={player_id}
        """

        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def get_players(self, filters: PlayersRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_filters(filters)
        success, result = self.__client.execute_query(query, return_results=True)

        if not success:
            return False, []

        players = [
            PlayerDAO.from_tuple(player_tuple=player_data) for player_data in result
        ]

        return True, players

    def delete_players(self, player_id: str) -> str | PlayerDoesNotExist:
        query = f"DELETE FROM {TABLE_NAME} WHERE playerid='{player_id}'"
        success = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def player_exists(
        self, player_id=None, first_name=None, last_name=None
    ) -> str | PlayerDoesNotExist:
        query = f"SELECT playerid FROM {TABLE_NAME} WHERE "

        if player_id is None:
            # Perform query with first and last name
            query += f"firstname='{first_name}' AND lastname='{last_name}'"
        else:
            query += f"playerid='{player_id}'"

        success, player = self.__client.execute_query(query, return_results=True)

        if not success:
            raise PlayerDoesNotExist(
                f"""
                Player does not exist with these fields: 
                    playerid: {player_id}, first_name: {first_name}, last_name: {last_name}
                """
            )

        if len(player) == 0 or player is None:
            raise PlayerDoesNotExist(
                f"Could not find player with provided fields: {player_id}, {first_name} {last_name}"
            )

        return player[0][0]

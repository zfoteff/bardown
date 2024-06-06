from datetime import datetime
from typing import List, Tuple
from uuid import NAMESPACE_OID, uuid5

from bin.logger import Logger
from config.db_config import PLAYER_TABLE_DB_CONFIG
from connectors.mysql import MySQLClient
from errors.players_errors import PlayerAlreadyExists, PlayerDoesNotExist
from players import PLAYERS_TABLE_NAME
from players.models.dao.player import Player as PlayerDAO
from players.models.dto.player import Player as PlayerDTO
from players.models.players_request_filters import PlayersRequestFilters

logger = Logger("db")


class PlayerDatabaseInterface:
    def __init__(self):
        self.__client = MySQLClient(**PLAYER_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def _build_query_from_filters(self, filters: PlayersRequestFilters) -> str:
        query = f"SELECT * FROM {PLAYERS_TABLE_NAME}"

        if filters.player_id is not None:
            query += f" WHERE playerid='{filters.player_id}'"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def create_player(self, player: PlayerDTO) -> bool | PlayerAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_player_id = str(
            uuid5(namespace=NAMESPACE_OID, name=player.first_name + player.last_name)
        )

        exists, player_id = self.player_exists(
            first_name=player.first_name, last_name=player.last_name
        )

        if exists:
            raise PlayerAlreadyExists("Player already exists", existing_player_id=player_id)

        query = f"""
            INSERT INTO {PLAYERS_TABLE_NAME}
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
            return False

        player.player_id = new_player_id
        player.created = create_modify_time
        player.modified = create_modify_time
        return True

    def update_player(self, player: PlayerDTO, player_id: str) -> bool | PlayerDoesNotExist:
        # TODO Complete patch to merge existing fields with null fields
        exists, player_id = self.player_exists(player_id)

        if exists is False:
            raise PlayerDoesNotExist(f"Player does not exist with this id: {player_id}")

        query = f"""
            UPDATE {PLAYERS_TABLE_NAME}
            SET number={player.number},
                first_name="{player.first_name}",
                last_name="{player.last_name}",
                position="{player.position}",
                grade="{player.grade}",
                school="{player.school}",
                modified='{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            WHERE playerid={player_id}
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

        players = [PlayerDAO.from_tuple(player_tuple=player_data) for player_data in result]

        return True, players

    def delete_players(self, player_id: str) -> str | PlayerDoesNotExist:
        query = f"DELETE FROM {PLAYERS_TABLE_NAME} WHERE playerid='{player_id}'"
        success = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def player_exists(
        self, player_id: str = None, first_name: str = None, last_name: str = None
    ) -> Tuple[bool, str | None]:
        """Check whether a player exists in the database

        Args:
            player_id (str, optional): Player id to query database for. Defaults to None.
            first_name (str, optional): Firstname to query database for. Defaults to None.
            last_name (str, optional): Lastname to query database for. Defaults to None.

        Returns:
            Tuple[bool, str | None]: Tuple containing a boolean asserting the player's
            existance, and the associated player id if applicable
        """
        query = f"SELECT playerid FROM {PLAYERS_TABLE_NAME} WHERE "

        if player_id is None:
            # Perform query with first and last name
            query += f"firstname='{first_name}' AND lastname='{last_name}'"
        else:
            # Perform query with player id
            query += f"playerid='{player_id}'"

        success, player = self.__client.execute_query(query, return_results=True)

        if not success or (len(player) == 0 or player is None):
            # If no player is found with the provided fields, return false and a null id
            return False, None

        return True, player[0][0]

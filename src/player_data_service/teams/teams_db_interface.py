from datetime import datetime
from typing import List, Tuple
from uuid import NAMESPACE_OID, uuid5

from teams import TEAMS_TABLE_NAME
from bin.logger import Logger
from config.db_config import TEAMS_TABLE_DB_CONFIG
from connectors.mysql import MySQLClient

logger = Logger("db")


class TeamsDBInterface:
    def __init__(self):
        self.__client = MySQLClient(**TEAMS_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def _build_query_from_filters(self, filters: TeamsRequestFilters) -> str:
        query = f"SELECT * FROM {TEAMS_TABLE_NAME}"

        return query

    def _build_update_fields(self, team: TeamDTO) -> str:
        modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        team_dict = {}

        return ""

    def create_game(self, team) -> bool | TeamAlreadyExists:
        pass

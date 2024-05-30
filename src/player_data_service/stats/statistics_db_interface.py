__version__ = "1.0.0"
__author__ = "Zac Foteff"

from datetime import datetime
from typing import List, Tuple

from bin.logger import Logger
from config.db_config import (
    SEASON_STATISTICS_TABLE_DB_CONFIG,
    STATISTICS_TABLE_DB_CONFIG,
)
from connectors.mysql import MySQLClient
from errors.statistics_errors import GameStatisticsAlreadyExist
from stats.__init___ import GAME_STATISTICS_TABLE_NAME
from stats.models.dto.statistics import GameStatistics
from stats.models.statistics_request_filters import GameStatisticsRequestFilters

logger = Logger("statistics-db-interface")


class StatisticsDatabaseInterface:
    def __init__(self):
        self.__game_client = MySQLClient(**STATISTICS_TABLE_DB_CONFIG)
        self.__season_client = MySQLClient(**SEASON_STATISTICS_TABLE_DB_CONFIG)
        self.__game_client.open_connection()
        self.__season_client.open_connection()

    def __enter__(self) -> None:
        self.__game_client.open_connection()
        self.__season_client.open_connection()

    def __exit__(self) -> None:
        self.__game_client.close_connection()
        self.__season_client.close_connection()

    def _build_query_from_filters(filters: GameStatisticsRequestFilters) -> str:
        query = f"SELECT * FROM {GAME_STATISTICS_TABLE_NAME}"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def create_game_statistic(
        self, player_id: str, game_id: str, statistics: GameStatistics
    ) -> bool | GameStatisticsAlreadyExist:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
            INSERT INTO {GAME_STATISTICS_TABLE_NAME}
            VALUES (
                "{player_id}",
                "{game_id}",
                "{str(statistics)}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__game_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def get_game_statistics(
        self, filters: GameStatisticsRequestFilters
    ) -> Tuple[bool, List]:
        query = self._build_query_from_filters(filters)
        success, result = self.__game_client.execute_query(query, return_results=True)

        if not success:
            return False, []

        game_stats = []

        return True, game_stats

from datetime import datetime
from typing import List, Tuple

from bin.logger import Logger
from config.db_config import (
    SEASON_STATISTICS_TABLE_DB_CONFIG,
    STATISTICS_TABLE_DB_CONFIG,
)
from connectors.mysql import MySQLClient
from errors.statistics_errors import (
    GameStatisticsAlreadyExist,
    GameStatisticsDoNoExist,
    StatisticsAlreadyExist,
    StatisticsDoNoExist,
)
from stats.__init___ import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME
from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dao.season_statistics import SeasonStatistics as SeasonStatisticsDAO
from stats.models.dto.game_statistics import GameStatistics as GameStatisticsDTO
from stats.models.dto.season_statistics import SeasonStatistics as SeasonStatisticsDTO
from stats.models.statistics_request_filters import (
    CompositeStatisticsRequestFilters,
    GameStatisticsRequestFilters,
    SeasonStatisticsRequestFilters,
)

logger = Logger("db")


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

    def _build_query_from_game_statistics_filters(
        self, filters: GameStatisticsRequestFilters
    ) -> str:
        query = f"SELECT * FROM {GAME_STATISTICS_TABLE_NAME}"

        if filters.player_id is not None and filters.game_id is None:
            query += f" WHERE playerid='{filters.player_id}'"

        if filters.player_id is None and filters.game_id is not None:
            query += f" WHERE gameid='{filters.game_id}'"

        if filters.player_id is not None and filters.game_id is not None:
            query += f" WHERE playerid='{filters.player_id}' AND gameid='{filters.game_id}'"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def _build_query_from_season_statistics_filters(
        self, filters: SeasonStatisticsRequestFilters
    ) -> str:
        query = f"SELECT * FROM {SEASON_STATISTICS_TABLE_NAME}"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def create_game_statistic(
        self, statistics: GameStatisticsDTO
    ) -> bool | GameStatisticsAlreadyExist:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
            INSERT INTO {GAME_STATISTICS_TABLE_NAME}
            VALUES (
                "{statistics.player_id}",
                "{statistics.game_id}",
                "{str(statistics.statistics)}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__game_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def create_season_statistics(
        self, statistics: SeasonStatisticsDTO
    ) -> bool | StatisticsAlreadyExist:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
            INSERT INTO {SEASON_STATISTICS_TABLE_NAME}
            VALUES (
                "{statistics.player_id}",
                "{statistics.team_id}",
                {statistics.year},
                "{str(statistics.statistics)}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__season_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def get_game_statistics(self, filters: GameStatisticsRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_game_statistics_filters(filters)
        success, result = self.__game_client.execute_query(query, return_results=True)

        if not success:
            return False, []

        game_stats = [
            GameStatisticsDAO.from_tuple(game_statistics_tuple=game_statistics_data)
            for game_statistics_data in result
        ]

        return True, game_stats

    def get_season_statistics(self, filters: SeasonStatisticsRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_season_statistics_filters(filters)
        success, result = self.__season_client.execute_query(query, return_results=True)

        if not success:
            return False, []

        season_stats = [
            SeasonStatisticsDAO.from_tuple(season_statistics_tuple=season_statistics_data)
            for season_statistics_data in result
        ]

        return True, season_stats

    def get_composite_statistics_for_player(
        filters: CompositeStatisticsRequestFilters,
    ) -> Tuple[bool, List]:
        pass

    def update_game_statistics(
        self, player_id: str, game_statistics: GameStatisticsDTO
    ) -> str | GameStatisticsDoNoExist:
        pass

    def update_season_statistics(
        self, player_id: str, game_statistics: GameStatisticsDTO
    ) -> str | GameStatisticsDoNoExist:
        pass

    def delete_game_statistics(self, player_id: str, game_id: str) -> str | StatisticsDoNoExist:
        query = f"DELETE FROM {SEASON_STATISTICS_TABLE_NAME} WHERE playerid='{player_id}' AND gameid='{game_id}'"
        success = self.__game_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def delete_season_statistics(
        self, player_id: str, team_id: str, year: str
    ) -> str | StatisticsDoNoExist:
        query = f"""
        DELETE FROM {SEASON_STATISTICS_TABLE_NAME} 
        WHERE playerid='{player_id}' AND teamid='{team_id}' AND year='{year}'
        """
        success = self.__season_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

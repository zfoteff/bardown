from datetime import datetime
from typing import List, Tuple

import config.player_data_service_config as application_config
from connectors.mysql import MySQLClient
from errors.statistics_errors import (
    GameStatisticsAlreadyExist,
    GameStatisticsDoNoExist,
    StatisticsAlreadyExist,
    StatisticsDoNoExist,
)
from fastapi import Depends
from stats import GAME_STATISTICS_TABLE_NAME, SEASON_STATISTICS_TABLE_NAME
from stats.models.dao.composite_game_statistics import CompositeGameStatistics
from stats.models.dao.composite_season_statistics import CompositeSeasonStatistics
from stats.models.dao.composite_statistics import CompositeStatistics
from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dao.season_statistics import SeasonStatistics as SeasonStatisticsDAO
from stats.models.dto.game_statistics import GameStatistics as GameStatisticsDTO
from stats.models.dto.season_statistics import SeasonStatistics as SeasonStatisticsDTO
from stats.models.statistics_request_filters import (
    CompositeStatisticsRequestFilters,
    GameStatisticsRequestFilters,
    SeasonStatisticsRequestFilters,
)
from typing_extensions import Annotated


class StatisticsDatabaseInterface:
    def __init__(
        self,
        config: application_config.PlayerDataServiceBaseConfig = Annotated[
            application_config.get_config(), Depends(application_config.get_config())
        ],
    ) -> None:
        self.__game_client = MySQLClient(
            user=config.mysql_user,
            password=config.mysql_password,
            host=config.mysql_host,
            database=config.mysql_database,
            table=GAME_STATISTICS_TABLE_NAME,
        )
        self.__season_client = MySQLClient(
            user=config.mysql_user,
            password=config.mysql_password,
            host=config.mysql_host,
            table=SEASON_STATISTICS_TABLE_NAME,
        )
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

    def _build_query_from_composite_statistics_filters(
        self, filters: CompositeStatisticsRequestFilters
    ) -> Tuple[str]:
        game_query = f"""
            select
                s.gameid, g.title, p.playerid, s.statistics
            from players p
                inner join game_statistics as s on p.playerid=s.playerid
                inner join games as g on s.gameid=g.gameid
            where 
                p.playerid="{filters.player_id}"
            order by g.created ASC
        """

        season_query = f"""
            select
                tp.teamid, t.name, p.playerid, s.year, s.statistics
            from
                players p
                inner join team_player tp on p.playerid = tp.playerid
                inner join teams t on t.teamid=tp.teamid
                inner join season_statistics s on p.playerid = s.playerid and tp.teamid = s.teamid
            where 
                p.playerid="{filters.player_id}"
            order by year DESC
        """

        return game_query, season_query

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
        self,
        filters: CompositeStatisticsRequestFilters,
    ) -> Tuple[bool, CompositeStatistics] | StatisticsDoNoExist:
        game_query, season_query = self._build_query_from_composite_statistics_filters(filters)
        game_success, game_result = self.__game_client.execute_query(
            game_query, return_results=True
        )
        season_success, season_result = self.__season_client.execute_query(
            season_query, return_results=True
        )

        query_success = True

        if not game_success:
            query_success = False
            game_result = []

        if not season_success:
            query_success = False
            season_result = []

        game_stats = [
            CompositeGameStatistics.from_tuple(
                composite_statistics_tuple=composite_game_statistics_data
            )
            for composite_game_statistics_data in game_result
        ]
        season_stats = [
            CompositeSeasonStatistics.from_tuple(
                composite_statistics_tuple=composite_season_statistics_data
            )
            for composite_season_statistics_data in season_result
        ]

        return query_success, CompositeStatistics(game_stats=game_stats, season_stats=season_stats)

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

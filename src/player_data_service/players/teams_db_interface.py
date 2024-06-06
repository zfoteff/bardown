from datetime import datetime
from typing import List, Tuple
from uuid import NAMESPACE_OID, uuid5

from bin.logger import Logger
from config.db_config import TEAMS_TABLE_DB_CONFIG
from connectors.mysql import MySQLClient
from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist
from players import TEAMS_TABLE_NAME
from players.models.dao.team import Team as TeamDAO
from players.models.dto.team import Team as TeamDTO
from players.models.teams_request_filters import TeamsRequestFilters

logger = Logger("db")


class TeamsDatabaseInterface:
    def __init__(self):
        self.__client = MySQLClient(**TEAMS_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def close_connection(self):
        self.__client.close_connection()

    def _build_query_from_filters(self, filters: TeamsRequestFilters) -> str:
        query = f"SELECT * FROM {TEAMS_TABLE_NAME}"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def create_team(self, team: TeamDTO) -> bool | TeamAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_team_id = str(uuid5(namespace=NAMESPACE_OID, name=team.name))
        query = f"""
            INSERT INTO {TEAMS_TABLE_NAME}
            VALUES (
                "{new_team_id}",
                "{team.name}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        team.team_id = new_team_id
        team.created = create_modify_time
        team.modified = create_modify_time
        return True

    def get_team(self, filters: TeamsRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_filters(filters)
        success, result = self.__client.execute_query(query, return_results=True)

        if not success:
            return False, []

        teams = [TeamDAO.from_tuple(team_tuple=team_data) for team_data in result]

        return True, teams

    def update_team(self, team_id: str, team: TeamDTO) -> str | TeamDoesNotExist:
        team_id = self.team_exists(team_id)
        query = f"""
            UPDATE {TEAMS_TABLE_NAME}
            SET name="{team.name}",
                modified="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
            WHERE teamid={team_id}
        """
        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def delete_team(self, team_id: str) -> str | TeamDoesNotExist:
        query = f"DELETE FROM {TEAMS_TABLE_NAME} WHERE teamid='{team_id}'"
        success = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def team_exists(self, team_id: str = None, name: str = None) -> str | TeamDoesNotExist:
        query = f"SELECT teamid FROM {TEAMS_TABLE_NAME} WHERE "

        if team_id is None:
            query += f"name='{name}'"

        else:
            query += f"teamid='{team_id}'"

        success, team = self.__client.execute_query(query, return_results=True)

        if not success or (len(team) == 0 or team is None):
            raise TeamDoesNotExist(
                f"""
                Team does not exist with these fields:
                    team_id: {team_id}, name: {name}
                """
            )

        return team[0][0]

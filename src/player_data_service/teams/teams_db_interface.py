from datetime import datetime
from typing import List, Self, Tuple
from uuid import NAMESPACE_OID, uuid5

import config.player_data_service_config as application_config
from connectors.mysql import MySQLClient
from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist
from fastapi import Depends
from teams import TEAMS_TABLE_NAME
from teams.models.dao.team import Team as TeamDAO
from teams.models.dto.team import Team as TeamDTO
from teams.models.team_request_filters import TeamRequestFilters
from typing_extensions import Annotated

from bin.logger import Logger
from utils.db_utils import build_update_fields

logger = Logger("db")


class TeamsDBInterface:
    def __init__(
        self,
        config: application_config.PlayerDataServiceBaseConfig = Annotated[
            application_config.get_config(), Depends(application_config.get_config())
        ],
    ) -> Self:
        self.__client = MySQLClient(
            host=config.mysql_host,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            table=TEAMS_TABLE_NAME,
        )
        self.__client.open_connection()

    def _build_query_from_filters(self, filters: TeamRequestFilters) -> str:
        query = f"SELECT * FROM {TEAMS_TABLE_NAME}"

        if filters.team_id is not None:
            query += f" WHERE teamid='{filters.team_id}'"

        if filters.name is not None:
            query += f" WHERE name='{filters.name}'"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def _build_update_query(self, team: TeamDTO, team_id: str) -> str:
        update_fields = build_update_fields(team)
        query = f"UPDATE {TEAMS_TABLE_NAME} SET {update_fields} WHERE teamid='{team_id}'"
        return query

    def create_team(self, team: TeamDTO) -> bool | TeamAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_team_id = str(uuid5(namespace=NAMESPACE_OID, name=team.name))

        exists, team_id = self.team_exists(team_name=team.name)

        if exists:
            raise TeamAlreadyExists("Team already exists", existing_team_id=team_id)

        query = f"""
            INSERT INTO {TEAMS_TABLE_NAME}
            VALUES (
                "{new_team_id}",
                "{team.name}",
                "{team.location}",
                "{team.img_url}",
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

    def get_team(self, filters: TeamRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_filters(filters)
        success, result = self.__client.execute_query(query, return_results=True)

        if not success:
            return False, []

        teams = [TeamDAO.from_tuple(team_data) for team_data in result]

        return True, teams

    # def get_composite_teams(self, filters: CompositeTeamRequestFilters) -> Tuple[bool, List]

    def update_team(self, team: TeamDTO, team_id: str) -> str | TeamDoesNotExist:
        team_id = self.team_exists(team_id)
        query = self._build_update_query(team, team_id)
        success, _ = self.__client.execute_query(query, commit_candidate=True)
        return True if not success else False

    def delete_team(self, team_id: str) -> str | TeamDoesNotExist:
        team_id = self.team_exists(team_id)
        query = f"DELETE FROM {TEAMS_TABLE_NAME} WHERE teamid='{team_id}'"
        success = self.__client.execute_query(query, commit_candidate=True)
        return True if not success else False

    def team_exists(self, team_id: str = None, team_name: str = None) -> str | TeamDoesNotExist:
        query = f"SELECT teamid FROM {TEAMS_TABLE_NAME} WHERE "

        if team_id is None:
            query += f"name='{team_name}'"
        else:
            query += f"teamid='{team_id}'"

        success, team = self.__client.execute_query(query, return_results=True)

        if not success or (len(team) == 0 or team is None):
            raise TeamDoesNotExist(
                f"""
                Team does not exist with these fields:
                    team_id: {team_id}, team_name: {team_name}
                """
            )

        return team[0][0]

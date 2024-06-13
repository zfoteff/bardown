from datetime import datetime
from typing import List, Tuple
from uuid import NAMESPACE_OID, uuid5

from bin.logger import Logger
from config.db_config import TEAMS_TABLE_DB_CONFIG
from connectors.mysql import MySQLClient
from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist
from teams import TEAMS_TABLE_NAME
from teams.models.dao.team import Team as TeamDAO
from teams.models.dto.team import Team as TeamDTO
from teams.models.team_request_filters import TeamRequestFilters

logger = Logger("db")


class TeamsDBInterface:
    def __init__(self):
        self.__client = MySQLClient(**TEAMS_TABLE_DB_CONFIG)
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

    def _build_update_fields(self, team: TeamDTO) -> str:
        modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        team_dict = {}

        for k, v in dict(team).items():
            if v is not None:
                team_dict[k] = v

        update_fields = [f"{k}='{v}'" for k, v in dict(team_dict).items()]
        update_fields.append(f"modified='{modify_time}'")
        return ", ".join(update_fields)

    def _build_update_query(self, team: TeamDTO, team_id: str) -> str:
        update_fields = self._build_update_fields(team)
        query = f"UPDATE {TEAMS_TABLE_NAME} SET {update_fields} WHERE teamid='{team_id}'"
        return query

    def create_team(self, team: TeamDTO) -> bool | TeamAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_team_id = str(uuid5(namespace=NAMESPACE_OID, name=team.name))

        exists, team_id = self.team_exists(name=team.name)

        if exists:
            raise TeamAlreadyExists("Team already exists", existing_team_id=team_id)

        query = f"""
            INSERT INTO {TEAMS_TABLE_NAME}
            VALUES (
                "{new_team_id}",
                "{team.name}",
                "{team.location}",
                "{team.imgurl}",
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

    def update_team(self, team: TeamDTO, team_id: str) -> str | TeamDoesNotExist:
        exists, team_id = self.team_exists(team_id)

        if exists is False:
            raise TeamDoesNotExist(f"Team does not exists with this id: {team_id}")

        query = self._build_update_query(team, team_id)
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

    def team_exists(self, team_id: str = None, name: str = None) -> Tuple[bool, str | None]:
        query = f"SELECT teamid FROM {TEAMS_TABLE_NAME} WHERE "

        if team_id is None:
            # Perform query with title and date
            query += f"name='{name}'"
        else:
            # Perform query with team id
            query += f"teamid='{team_id}'"

        success, team = self.__client.execute_query(query, return_results=True)

        if not success or (len(team) == 0 or team is None):
            return False, None

        return True, team[0][0]

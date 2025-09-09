from datetime import datetime
from typing import List, Self, Tuple
from uuid import NAMESPACE_OID, uuid5

import config.player_data_service_config as application_config
from connectors.mysql import MySQLClient
from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist
from fastapi import Depends
from teams import TEAMS_TABLE_NAME, TEAM_PLAYER_TABLE_NAME
from players import PLAYERS_TABLE_NAME
from teams.models.dao.composite_team import CompositeTeam
from teams.models.dao.team import Team as TeamDAO
from teams.models.dto.team import Team as TeamDTO
from teams.models.dto.team_player import TeamPlayer
from teams.models.team_request_filters import CompositeTeamRequestFilters, TeamRequestFilters
from typing_extensions import Annotated

from bin.logger import Logger
from utils.db_utils import build_update_fields

logger = Logger("db")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class TeamsDBInterface:
    def __init__(
        self,
        config: application_config.PlayerDataServiceBaseConfig = Annotated[
            application_config.get_config(), Depends(application_config.get_config())
        ],
    ) -> Self:
        self.__teams_client = MySQLClient(
            host=config.mysql_host,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            table=TEAMS_TABLE_NAME,
        )
        self.__players_client = MySQLClient(
            host=config.mysql_host,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            table=PLAYERS_TABLE_NAME,
        )
        self.__team_players_client = MySQLClient(
            host=config.mysql_host,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            table=TEAM_PLAYER_TABLE_NAME,    
        )

    def __enter__(self) -> None:
        self.__teams_client.open_connection()
        self.__players_client.open_connection()
        self.__team_players_client.open_connection()

    def __exit__(self) -> None:
        self.__teams_client.close_connection()
        self.__players_client.close_connection()
        self.__team_players_client.close_connection()

    def _build_team_query_from_filters(self, filters: TeamRequestFilters | CompositeTeamRequestFilters) -> str:
        query = f"SELECT * FROM {TEAMS_TABLE_NAME}"

        if filters.team_id is not None:
            query += f" WHERE teamid='{filters.team_id}'"

        if filters.team_name is not None:
            query += f" WHERE name='{filters.team_name}'"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def _build_composite_team_players_query_from_filters(self, filter: CompositeTeamRequestFilters) -> str:
        where_clause = "WHERE tp.teamid={filter.team_id}" if filter.team_id is not None else "WHERE tp.playerid={filter.player_id}"

        query = f"""
            SELECT 
                tp.teamid, tp.year, p.playerid, p.firstname, p.lastname,
                tp.number, p.position, p.grade, p.school, p.imgurl
            FROM {TEAM_PLAYER_TABLE_NAME} as tp
            {where_clause}
            ORDER BY tp.year DESC
        """

    def _build_update_query(self, team: TeamDTO, team_id: str) -> str:
        update_fields = build_update_fields(team)
        query = f"UPDATE {TEAMS_TABLE_NAME} SET {update_fields} WHERE teamid='{team_id}'"
        return query

    def create_team(self, team: TeamDTO) -> bool | TeamAlreadyExists:
        create_modify_time = datetime.now().strftime(DATETIME_FORMAT)
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

        success, _ = self.__teams_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        team.team_id = new_team_id
        team.created = create_modify_time
        team.modified = create_modify_time
        return True
    
    def add_player_to_team(self, team_player_data: TeamPlayer) -> bool:
        create_modify_time = datetime.now().strftime(DATETIME_FORMAT)
        team_exists, team_id = self.team_exists(team_id=team_id)
        
        if not team_exists:
            raise TeamDoesNotExist(f"Team does not exist with id: {team_id}")

        query = f"""
            INSERT INTO {TEAM_PLAYER_TABLE_NAME}
            VALUES (
                "{team_player_data.team_id}",
                "{team_player_data.player_id}",
                {team_player_data.year},
                {team_player_data.number},
                "{str(team_player_data.position)}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__team_players_client.execute_query(query, commit_candidate=True)
        
        if not success:
            return False

        team_player_data.created = create_modify_time 
        team_player_data.modified = create_modify_time
        return success

    def get_team(self, filters: TeamRequestFilters | CompositeTeamRequestFilters) -> Tuple[bool, List]:
        query = self._build_team_query_from_filters(filters)
        success, result = self.__teams_client.execute_query(query, return_results=True)

        if not success:
            return False, []

        teams = [TeamDAO.from_tuple(team_data) for team_data in result]

        return True, teams

    def get_composite_teams(self, filters: CompositeTeamRequestFilters) -> Tuple[bool, List[CompositeTeam]] | TeamDoesNotExist:
        team_exists, team = self.get_team(filters)

        if not team_exists:
            raise TeamDoesNotExist(f"Team with id {filters.team_id} does not exist")

        player_query = self._build_composite_team_players_query_from_filters(filters)
        coaches_query = self._build_composite_team_player_query_from_filters(filters)


    def update_team(self, team: TeamDTO, team_id: str) -> str | TeamDoesNotExist:
        team_id = self.team_exists(team_id)
        query = self._build_update_query(team, team_id)
        success, _ = self.__teams_client.execute_query(query, commit_candidate=True)
        return True if not success else False

    def delete_team(self, team_id: str) -> str | TeamDoesNotExist:
        team_id = self.team_exists(team_id)
        query = f"DELETE FROM {TEAMS_TABLE_NAME} WHERE teamid='{team_id}'"
        success = self.__teams_client.execute_query(query, commit_candidate=True)
        return True if not success else False

    def team_exists(self, team_id: str = None, team_name: str = None) -> str | TeamDoesNotExist:
        query = f"SELECT teamid FROM {TEAMS_TABLE_NAME} WHERE "

        if team_id is None:
            query += f"name='{team_name}'"
        else:
            query += f"teamid='{team_id}'"

        success, team = self.__teams_client.execute_query(query, return_results=True)

        if not success or (len(team) == 0 or team is None):
            raise TeamDoesNotExist(
                f"""
                Team does not exist with these fields:
                    team_id: {team_id}, team_name: {team_name}
                """
            )

        return team[0][0]

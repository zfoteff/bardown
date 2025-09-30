from datetime import datetime
from typing import List, Self, Tuple
from uuid import NAMESPACE_OID, uuid5

import config.player_data_service_config as application_config
from connectors.mysql import MySQLClient
from errors.coaches_errors import CoachDoesNotExist
from errors.players_errors import PlayerDoesNotExist
from errors.teams_errors import TeamAlreadyExists, TeamDoesNotExist
from fastapi import Depends
from players import COACHES_TABLE_NAME, PLAYERS_TABLE_NAME
from teams import TEAM_COACH_TABLE_NAME, TEAM_PLAYER_TABLE_NAME, TEAMS_TABLE_NAME
from teams.models.dao.composite_team import (
    CompositeTeam,
    CompositeTeamCoach,
    CompositeTeamPlayer,
)
from teams.models.dao.team import Team as TeamDAO
from teams.models.dto.team import Team as TeamDTO
from teams.models.dto.team_coach import TeamCoach
from teams.models.dto.team_player import TeamPlayer
from teams.models.team_request_filters import (
    CompositeTeamRequestFilters,
    TeamRequestFilters,
)
from typing_extensions import Annotated
from bin.db_utils import build_update_fields

from bin.logger import Logger

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
        self.__team_coaches_client = MySQLClient(
            host=config.mysql_host,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            table=TEAM_COACH_TABLE_NAME,
        )
        self.__teams_client.open_connection()
        self.__players_client.open_connection()
        self.__team_players_client.open_connection()
        self.__team_coaches_client.open_connection()

    def __exit__(self) -> None:
        self.__teams_client.close_connection()
        self.__players_client.close_connection()
        self.__team_players_client.close_connection()
        self.__team_coaches_client.open_connection()

    def _build_team_query_from_filters(
        self, filters: TeamRequestFilters | CompositeTeamRequestFilters
    ) -> str:
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

    def _build_composite_team_players_query_from_filters(
        self, filter: CompositeTeamRequestFilters
    ) -> str:
        where_clause = (
            f"WHERE tp.teamid='{filter.team_id}'"
            if filter.team_id is not None
            else f"WHERE tp.playerid='{filter.player_id}'"
        )

        return f"""
            SELECT 
                tp.teamid, t.name, t.location, t.imgurl, 
                tp.year, p.playerid, p.firstname, p.lastname,
                tp.number, p.position, p.grade, p.school, p.imgurl
            FROM {TEAM_PLAYER_TABLE_NAME} as tp
                INNER JOIN {PLAYERS_TABLE_NAME} as p on p.playerid=tp.playerid
                INNER JOIN {TEAMS_TABLE_NAME} as t on t.teamid=tp.teamid
            {where_clause}
            ORDER BY tp.year DESC
        """

    def _build_composite_team_coaches_query_from_filters(
        self, filter: CompositeTeamRequestFilters
    ) -> str:
        where_clause = (
            f"WHERE tc.teamid='{filter.team_id}'"
            if filter.team_id is not None
            else f"WHERE tc.coachid='{filter.coach_id}'"
        )

        return f"""
            SELECT
                tc.teamid, t.name, t.location, t.imgurl, 
                tc.year, c.coachid, c.firstname, c.lastname,
                tc.role, tc.since, c.email, c.phonenumber, c.imgurl
            FROM {TEAM_COACH_TABLE_NAME} as tc
                INNER JOIN {COACHES_TABLE_NAME} as c on c.coachid=tc.coachid
                INNER JOIN {TEAMS_TABLE_NAME} as t on t.teamid=tc.teamid
            {where_clause}
            ORDER BY tc.year DESC
        """

    def _build_update_query(self, team: TeamDTO, team_id: str) -> str:
        update_fields = build_update_fields(team)
        query = f"UPDATE {TEAMS_TABLE_NAME} SET {update_fields} WHERE teamid='{team_id}'"
        return query

    def create_team(self, team: TeamDTO) -> bool | TeamAlreadyExists:
        create_modify_time = datetime.now().strftime(DATETIME_FORMAT)
        new_team_id = str(uuid5(namespace=NAMESPACE_OID, name=team.name))

        try:
            exists, team_id = self.team_exists(team_name=team.name)
            if exists:
                raise TeamAlreadyExists("Team already exists", existing_team_id=team_id)
        except TeamDoesNotExist:
            pass

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
        team_exists, team_id = self.team_exists(team_id=team_player_data.team_id)
        player_exists, player_id = self.player_exists(player_id=team_player_data.player_id)

        if not team_exists:
            raise TeamDoesNotExist(f"Team does not exist with id: {team_player_data.team_id}")

        if not player_exists:
            raise PlayerDoesNotExist(f"Player does not exist with id: {team_player_data.player_id}")

        query = f"""
            INSERT INTO {TEAM_PLAYER_TABLE_NAME}
            VALUES (
                "{team_id}",
                "{player_id}",
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

    def add_coach_to_team(self, team_coach_data: TeamCoach) -> bool:
        create_modify_time = datetime.now().strftime(DATETIME_FORMAT)
        team_exists, team_id = self.team_exists(team_id=team_coach_data.team_id)
        coach_exists, coach_id = self.coach_exists(coach_id=team_coach_data.coach_id)

        if not team_exists:
            raise TeamDoesNotExist(f"Team does not exist with id: {team_coach_data.team_id}")

        if not coach_exists:
            raise CoachDoesNotExist(f"Coach does not exist with id: {team_coach_data.coach_id}")

        query = f"""
            INSERT INTO {TEAM_COACH_TABLE_NAME}
            VALUES (
                "{team_id}",
                "{coach_id}",
                {team_coach_data.year},
                "{team_coach_data.role}",
                {team_coach_data.since},
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__team_coaches_client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        team_coach_data.created = create_modify_time
        team_coach_data.modified = create_modify_time
        return success

    def get_team(
        self, filters: TeamRequestFilters | CompositeTeamRequestFilters
    ) -> Tuple[bool, List]:
        query = self._build_team_query_from_filters(filters)
        success, result = self.__teams_client.execute_query(query, return_results=True)

        if not success:
            return False, []

        teams = [TeamDAO.from_tuple(team_data) for team_data in result]

        return True, teams

    def get_composite_teams(
        self, filters: CompositeTeamRequestFilters
    ) -> Tuple[bool, CompositeTeam] | TeamDoesNotExist:
        players_query = self._build_composite_team_players_query_from_filters(filters)
        coaches_query = self._build_composite_team_coaches_query_from_filters(filters)

        players_query_sucess, players_query_result = self.__team_players_client.execute_query(
            query=players_query, return_results=True
        )
        coaches_query_sucess, coaches_query_result = self.__team_coaches_client.execute_query(
            query=coaches_query, return_results=True
        )

        composite_query_success = True

        if not players_query_sucess:
            composite_query_success = False
            players_query_result = []

        if not coaches_query_sucess:
            composite_query_success = False
            coaches_query_result = []

        players = [
            CompositeTeamPlayer.from_tuple(composite_team_player_tuple=composite_team_player_data)
            for composite_team_player_data in players_query_result
        ]
        coaches = [
            CompositeTeamCoach.from_tuple(composite_team_coach_tuple=composite_team_coach_data)
            for composite_team_coach_data in coaches_query_result
        ]

        return composite_query_success, CompositeTeam(players=players, coaches=coaches)

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

    def player_exists(
        self, player_id: str = None, first_name: str = None, last_name: str = None
    ) -> str | PlayerDoesNotExist:
        query = f"SELECT playerid FROM {PLAYERS_TABLE_NAME} WHERE "

        if player_id is None:
            query += f"firstname='{first_name}' AND lastname='{last_name}'"
        else:
            query += f"playerid='{player_id}'"

        success, player = self.__players_client.execute_query(query, return_results=True)

        if not success or (len(player) == 0 or player is None):
            raise PlayerDoesNotExist(
                f"""
                Player does not exist with these fields:
                    player_id: {player_id}, first_name: {first_name}, last_name: {last_name}
                """
            )

        return player[0][0]

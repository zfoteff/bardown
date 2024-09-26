from datetime import datetime
from typing import List, Tuple
from uuid import NAMESPACE_OID, uuid5

from bin.logger import Logger
from config.db_config import GAMES_TABLE_DB_CONFIG
from connectors.mysql import MySQLClient
from errors.games_errors import GameAlreadyExists, GameDoesNotExist
from games import GAMES_TABLE_NAME
from games.models.dao.game import Game as GameDAO
from games.models.dto.game import Game as GameDTO
from games.models.game_request_filters import GameRequestFilters

logger = Logger("db")


class GamesDBInterface:
    def __init__(self):
        self.__client = MySQLClient(**GAMES_TABLE_DB_CONFIG)
        self.__client.open_connection()

    def _build_query_from_filters(self, filters: GameRequestFilters) -> str:
        query = f"SELECT * FROM {GAMES_TABLE_NAME}"

        if filters.game_id is not None:
            query += f" WHERE gameid='{filters.game_id}'"

        if filters.order is not None:
            query += f" ORDER BY {filters.order_by} {filters.order}"

        if filters.limit is not None:
            query += f" LIMIT {filters.limit}"

        if filters.offset is not None:
            query += f" OFFSET {filters.offset}"

        return query

    def _build_update_fields(self, game: GameDTO) -> str:
        modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        game_dict = {}

        for k, v in dict(game).items():
            if v is not None:
                game_dict[k] = v

        update_fields = [f"{k}='{v}'" for k, v in dict(game_dict).items()]
        update_fields.append(f"modified='{modify_time}'")
        return ", ".join(update_fields)

    def _build_update_query(self, game: GameDTO, game_id: str) -> str:
        update_fields = self._build_update_fields(game)
        query = (
            f"UPDATE {GAMES_TABLE_NAME} SET {update_fields} WHERE gameid='{game_id}'"
        )
        return query

    def create_game(self, game: GameDTO) -> bool | GameAlreadyExists:
        create_modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_game_id = str(
            uuid5(namespace=NAMESPACE_OID, name=str(game.date) + game.title)
        )

        exists, game_id = self.game_exists(title=game.title, date=game.date)

        if exists:
            raise GameAlreadyExists("Game already exists", existing_game_id=game_id)

        query = f"""
            INSERT INTO {GAMES_TABLE_NAME}
            VALUES (
                "{new_game_id}",
                "{game.title}",
                "{game.date}",
                "{game.score}",
                "{game.location}",
                "{create_modify_time}",
                "{create_modify_time}"
            )
        """

        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        game.game_id = new_game_id
        game.created = create_modify_time
        game.modified = create_modify_time
        return True

    def get_games(self, filters: GameRequestFilters) -> Tuple[bool, List]:
        query = self._build_query_from_filters(filters)
        success, result = self.__client.execute_query(query, return_results=True)

        if not success:
            return False, []

        games = [GameDAO.from_tuple(game_tuple=game_data) for game_data in result]

        return True, games

    def update_game(self, game: GameDTO, game_id: str) -> str | GameDoesNotExist:
        exists, game_id = self.game_exists(game_id)

        if exists is False:
            raise GameDoesNotExist(f"Game does not exist with this id: {game_id}")

        query = self._build_update_query(game, game_id)
        success, _ = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def delete_game(self, game_id: str) -> str | GameDoesNotExist:
        query = f"DELETE FROM {GAMES_TABLE_NAME} WHERE gameid='{game_id}'"
        success = self.__client.execute_query(query, commit_candidate=True)

        if not success:
            return False

        return True

    def game_exists(
        self, game_id: str = None, title: str = None, date: datetime = None
    ) -> Tuple[bool, str | None]:
        query = f"SELECT gameid FROM {GAMES_TABLE_NAME} WHERE "

        if game_id is None:
            # Perform query with title and date
            query += f"title='{title}' AND date='{date}'"
        else:
            # Perform query with game id
            query += f"gameid='{game_id}'"

        success, game = self.__client.execute_query(query, return_results=True)

        if not success or (len(game) == 0 or game is None):
            return False, None

        return True, game[0][0]

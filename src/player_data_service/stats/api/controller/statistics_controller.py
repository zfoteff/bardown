from bin.logger import Logger
from errors.statistics_errors import StatisticsAlreadyExist
from fastapi.responses import JSONResponse
from stats.models.dto.game_statistics import GameStatistics
from stats.statistics_db_interface import StatisticsDatabaseInterface

logger = Logger("player-data-service-controller")
db_interface = StatisticsDatabaseInterface()


class StatisticsController:
    async def create_game_statistics(
        player_id: str, game_id: str, statistics: GameStatistics
    ) -> JSONResponse:
        try:
            result = db_interface.create_game_statistic(player_id, game_id, GameStatistics)
        except StatisticsAlreadyExist as err:
            return JSONResponse(
                status_code=409,
                content={
                    "status": 409,
                    "error": {
                        "message": f"{err}",
                    },
                },
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=201,
            content={
                "status": 201,
                "data": {
                    "player_id": f"{player_id}",
                    "game_id": f"{game_id}",
                    "statistics": f"{str(statistics)}",
                },
            },
        )

    async def get_game_statistics(player_id: str, game_id: str) -> JSONResponse:
        pass

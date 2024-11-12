from typing import List, Tuple

from errors.statistics_errors import (
    StatisticsAlreadyExist,
    StatisticsDoNoExist,
    StatisticsValidationError,
)
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from stats.api.validators.statistics_query_validator import (
    validate_get_game_statistics_query_parameters,
    validate_get_season_statistics_query_parameters,
)
from stats.mappers.statistics_mapper import (
    game_statistics_DAO_to_game_statistics_DTO,
    season_statistics_DAO_to_season_statistics_DTO,
)
from stats.models.dto.game_statistics import GameStatistics
from stats.models.dto.season_statistics import SeasonStatistics
from stats.statistics_db_interface import StatisticsDatabaseInterface

from bin.logger import Logger

logger = Logger("player-data-service-controller")
db_interface = StatisticsDatabaseInterface()


class StatisticsController:
    async def create_game_statistics(statistics: GameStatistics) -> JSONResponse:
        try:
            result = db_interface.create_game_statistic(statistics)
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
            content={"status": 201, "data": jsonable_encoder(statistics)},
        )

    async def create_season_statistics(statistics: SeasonStatistics) -> JSONResponse:
        try:
            result = db_interface.create_season_statistics(statistics)
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
            content={"status": 201, "data": jsonable_encoder(statistics)},
        )

    async def get_game_statistics(request: Request) -> JSONResponse:
        try:
            filters = validate_get_game_statistics_query_parameters(request.query_params)
            result, statistics = db_interface.get_game_statistics(filters)
        except StatisticsDoNoExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(
                status_code=422,
                content={"status": 422, "error": {"message": "Database error"}},
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": []
                if (statistics == []) or (statistics is None)
                else [
                    jsonable_encoder(game_statistics_DAO_to_game_statistics_DTO(statistic))
                    for statistic in statistics
                ],
            },
        )

    async def get_season_statistics(request: Request) -> Tuple[bool, List]:
        try:
            filters = validate_get_season_statistics_query_parameters(request.query_params)
            result, statistics = db_interface.get_season_statistics(filters)
        except StatisticsValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(
                status_code=422, content={"status": 422, "error": {"message": f"{err}"}}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": []
                if (statistics == []) or (statistics is None)
                else [
                    jsonable_encoder(season_statistics_DAO_to_season_statistics_DTO(statistic))
                    for statistic in statistics
                ],
            },
        )

    async def delete_game_statistics(self, player_id: str, game_id: str) -> JSONResponse:
        try:
            result = db_interface.delete_game_statistics(player_id, game_id)
        except StatisticsDoNoExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": {"player_id": player_id, "game_id": game_id},
            },
        )

    async def delete_season_statistics(
        self, player_id: str, team_id: str, year: int
    ) -> JSONResponse:
        try:
            result = db_interface.delete_season_statistics(player_id, team_id, year)
        except StatisticsDoNoExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(status_code=422, content={"status": 422, "error": "Database error"})

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "data": {"player_id": player_id, "game_id": team_id, "year": year},
            },
        )

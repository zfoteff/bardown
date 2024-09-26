from fastapi import Request
from fastapi.encoders import jsonable_encoder
from bin.logger import Logger
from typing import List, Tuple
from errors.statistics_errors import StatisticsAlreadyExist, StatisticsDoNoExist
from fastapi.responses import JSONResponse
from stats.models.dao.season_statistics import SeasonStatistics
from stats.models.dto.game_statistics import GameStatistics
from stats.models.statistics_request_filters import SeasonStatisticsRequestFilters
from stats.statistics_db_interface import StatisticsDatabaseInterface
from stats.api.validators.game_statistics_query_validator import *
from stats.api.validators.season_statistics_query_validator import *

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
            filters = validate_get_game_statistics_parameters(request.query_params)
            result, statistics = db_interface.get_game_statistics(filters)
        except StatisticsDoNoExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": {"message": f"{err}"}}
            )

        if not result:
            return JSONResponse(
                status_code=403,
                content={"status": 403, "error": {"message": "Database error"}},
            )

        return JSONResponse(status_code=200, content={"status": 201, "data": {}})

    async def get_season_statistics(
        self, filters: SeasonStatisticsRequestFilters
    ) -> Tuple[bool, List]:
        try:
            filters = validate_get_season_statistics_parameters()

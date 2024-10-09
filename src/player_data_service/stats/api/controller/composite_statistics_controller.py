from typing import List, Tuple

from bin.logger import Logger
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from errors.statistics_errors import (
    StatisticsAlreadyExist,
    StatisticsDoNoExist,
    StatisticsValidationError,
)
from stats.models.dto.composite_statistics import CompositeStatistics
from stats.models.statistics_request_filters import CompositeStatisticsRequestFilters
from stats.statistics_db_interface import StatisticsDatabaseInterface

logger = Logger("player-data-service-controller")
db_interface = StatisticsDatabaseInterface()


class CompositeStatisticsController:
    async def get_composite_statistics(request: Request) -> JSONResponse:
        try:
            filters = validate_get_composite_statistics_query_parameters(request.query_params)
            result, statistics = db_interface.get_composite_statistics_for_player()
        except StatisticsDoNoExist as err:
            return JSONResponse(
                status_code=404, content={"status": 404, "error": {"message": f"{err}"}}
            )
        except StatisticsValidationError as err:
            return JSONResponse(
                status_code=400, content={"status": 400, "error": {"message": f"{err}"}}
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
                    jsonable_encoder(
                        composite_statistics_DAO_to_composite_statistics_DTO(statistic)
                    )
                    for statistic in statistics
                ],
            },
        )

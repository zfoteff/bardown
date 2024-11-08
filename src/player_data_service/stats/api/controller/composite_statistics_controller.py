from bin.logger import Logger
from errors.statistics_errors import StatisticsDoNoExist, StatisticsValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from stats.api.validators.statistics_query_validator import (
    validate_get_composite_statistics_query_parameters,
)
from stats.mappers.statistics_mapper import (
    composite_statistics_DAO_to_composite_statistics_DTO,
)
from stats.models.dto.composite_statistics import CompositeStatistics
from stats.models.statistics_request_filters import CompositeStatisticsRequestFilters
from stats.statistics_db_interface import StatisticsDatabaseInterface

logger = Logger("player-data-service-controller")
db_interface = StatisticsDatabaseInterface()


def is_player_provided(filters: CompositeStatisticsRequestFilters) -> bool:
    return filters.player_id is not None or (
        filters.player_first_name is not None and filters.player_last_name is not None
    )


class CompositeStatisticsController:
    async def get_composite_statistics(request: Request) -> JSONResponse:
        try:
            filters = validate_get_composite_statistics_query_parameters(request.query_params)

            if is_player_provided(filters):
                result, statistics = db_interface.get_composite_statistics_for_player(filters)
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
                "data": jsonable_encoder(
                    composite_statistics_DAO_to_composite_statistics_DTO(statistics)
                ),
            },
        )

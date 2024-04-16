import re
from typing import Tuple

from fastapi import Request

from src.player_data_service.errors.player_validation_error import PlayerValidationError
from src.player_data_service.players.models.dto.players_request_filters import (
    PlayersRequestFilters,
)

UUID_REGEX_PATTERN = (
    r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
)


def validate_get_players_query_parameters(
    request: Request,
) -> Tuple | PlayerValidationError:
    filters = PlayersRequestFilters()
    player_id = request.query_params.get("filter.playerId")
    first_name = request.query_params.get("filter.firstName")
    last_name = request.query_params.get("filter.lastName")
    limit = request.query_params.get("limit")
    offset = request.query_params.get("offset")
    order = request.query_params.get("order")
    order_by = request.query_params.get("orderBy")

    if player_id is not None:
        regex = re.compile(UUID_REGEX_PATTERN)
        match = regex.match(player_id)
        if match is None:
            raise PlayerValidationError("PlayerId must be in UUIDv4 format")

        filters.player_id = player_id

    if first_name is not None and last_name is not None:
        pass

    if _order_missing_pair(order, order_by):
        if order is None:
            raise PlayerValidationError(
                "Order parameter cannot be null when Order By parameter exists"
            )
        elif order_by is None:
            raise PlayerValidationError(
                "Order By parameter cannot be null when Order parameter exists"
            )
    elif not _order_equals_allowed_value(order):
        raise PlayerValidationError(
            'Order value must be one of the allowed values ["ASC", "DESC"]'
        )

    return filters


def _order_equals_allowed_value(order: str) -> bool:
    return order == "ASC" or order == "DESC"


def _order_missing_pair(order: str, orderBy: str) -> bool:
    return not (
        (order is None and orderBy is None)
        or (order is not None and orderBy is not None)
    )

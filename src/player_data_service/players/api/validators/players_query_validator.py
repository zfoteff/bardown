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
NAME_REGEX_PATTERN = r"^[A-Z]'?[- a-zA-Z]+$"


def _order_equals_allowed_value(order: str) -> bool:
    return order == "ASC" or order == "DESC"


def _order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None)
        or (order is not None and order_by is not None)
    )


def _name_missing_pair(first_name: str, last_name: str) -> bool:
    return not (
        (first_name is None and last_name is None)
        or (first_name is not None and last_name is not None)
    )


def validate_get_players_query_parameters(
    query_params: dict,
) -> Tuple | PlayerValidationError:
    filters = PlayersRequestFilters()

    # Get all query param values, or none if none provided
    player_id = query_params.get("filter.playerId")
    first_name = query_params.get("filter.firstName")
    last_name = query_params.get("filter.lastName")
    number = query_params.get("filter.number")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if player_id is not None:
        # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
        if type(player_id) != str:
            raise PlayerValidationError("PlayerId must be a string in UUIDv4 format")

        regex = re.compile(UUID_REGEX_PATTERN)
        player_id_matches = regex.match(player_id)
        if player_id_matches is None:
            raise PlayerValidationError("PlayerId must be a string in UUIDv4 format")

        filters.player_id = player_id

    if first_name is not None and last_name is not None:
        # Name filter validation. Both first and last name must be provided, and match regex filter
        if _name_missing_pair(first_name, last_name):
            if first_name is None:
                raise PlayerValidationError(
                    "filter.firstName must both be provided with filter.lastName to filter results."
                )

            if last_name is None:
                raise PlayerValidationError(
                    "filter.lastName must both be provided with filter.firstName to filter results."
                )

        regex = re.compile(NAME_REGEX_PATTERN)
        first_name_matches = regex.match(str.capitalize(first_name))
        last_name_matches = regex.match(str.capitalize(last_name))

        if first_name_matches is None:
            raise PlayerValidationError("filter.firstName is invalid.")

        if last_name_matches is None:
            raise PlayerValidationError("filter.lastName is invalid.")

        filters.first_name = first_name
        filters.last_name = last_name

    if number is not None:
        if number < 0:
            raise PlayerValidationError

        filters.number = number


    if limit is not None
        if limit < 0:
            # Limit validation, if provided. Must be a non-null, positive integer
            filters.limit = 10
        else:
            filters.limit = limit

    if offset is not None and offset < 0:
        offset = None

    filters.offset = offset

    if order is not None or order_by is not None:
        # Ordering rules. Both order direction and order by field must be provided, and match set of accepted values
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

        filters.order = order
        filters.order_by = order_by

    return filters

import re

from src.player_data_service.errors.players_errors import PlayerValidationError
from src.player_data_service.players.models.dto.players_request_filters import (
    PlayersRequestFilters,
)

UUID_REGEX_PATTERN = (
    r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
)
NAME_REGEX_PATTERN = r"^[A-Z]'?[- a-zA-Z]+$"


def _order_equals_allowed_value(order: str) -> bool:
    return order == "ASC" or order == "DESC"


def _order_by_equals_allowed_value(order_by: str) -> bool:
    valid_values = ["number", "first_name", "last_name", "grade", "school"]
    return str.lower(order_by) in valid_values


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


def _validate_player_id_filter(filters: PlayersRequestFilters, player_id: str) -> None:
    # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
    if type(player_id) != str:
        raise PlayerValidationError("PlayerId must be a string in UUIDv4 format")

    regex = re.compile(UUID_REGEX_PATTERN)
    player_id_matches = regex.match(player_id)
    if player_id_matches is None:
        raise PlayerValidationError("PlayerId must be a string in UUIDv4 format")

    filters.player_id = player_id


def _validate_name_filter(
    filters: PlayersRequestFilters, first_name: str, last_name: str
) -> None:
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


def _validate_number_filter(filters: PlayersRequestFilters, number: int) -> None:
    if int(number) < 0:
        raise PlayerValidationError("filter.number must be a positive integer")

    filters.number = number


def _validate_limit(filters: PlayersRequestFilters, limit: int) -> None:
    if int(limit) < 0:
        # Limit validation, if provided. Must be a non-null, positive integer
        filters.limit = 10
    else:
        filters.limit = limit


def _validate_offset(filters: PlayersRequestFilters, offset: int) -> None:
    if int(offset) < 0:
        offset = None

    filters.offset = offset


def _validate_ordering_rules(
    filters: PlayersRequestFilters, order: str, order_by: str
) -> None:
    # Ordering rules. Both order direction and order by field must be provided, and match set of accepted values
    if _order_missing_pair(order, order_by):
        if order is None:
            raise PlayerValidationError(
                "order parameter cannot be null when orderBy parameter exists"
            )
        elif order_by is None:
            raise PlayerValidationError(
                "orderBy parameter cannot be null when order parameter exists"
            )
    elif not _order_equals_allowed_value(order):
        raise PlayerValidationError(
            'order value must be one of the allowed values ["ASC", "DESC"]'
        )

    filters.order = str.upper(order)

    if not _order_by_equals_allowed_value(order_by):
        raise PlayerValidationError(
            "order query must be one of the allowed values ['first_name'. 'last_name', 'number']"
        )

    filters.order_by = str.lower(order_by)


def validate_get_players_query_parameters(
    query_params: dict,
) -> PlayersRequestFilters | PlayerValidationError:
    filters = PlayersRequestFilters()

    # Get all query param values, or none if none provided
    player_id = query_params.get("filter.playerId")
    first_name = query_params.get("filter.firstName")
    last_name = query_params.get("filter.lastName")
    number = query_params.get("filter.number")
    grade = query_params.get("filter.grade")
    position = query_params.get("filter.position")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if player_id is not None:
        _validate_player_id_filter(filters, player_id)

    if first_name is not None or last_name is not None:
        _validate_name_filter(filters, first_name, last_name)

    if number is not None:
        _validate_number_filter(filters, number)

    if limit is not None:
        _validate_limit(filters, limit)

    if offset is not None:
        _validate_offset(filters, offset)

    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters

import re
from datetime import datetime

from errors.games_errors import GameValidationError
from games.api.validators import BASIC_TEXT_REGEX_PATTERN, UUID_REGEX_PATTERN
from games.models.game_request_filters import GameRequestFilters


def _validate_limit(filters: GameRequestFilters, limit: int) -> None:
    """
    Limit validation, if provided. Must be a non-null, positive integer. Defaults to 25
    if no value provided
    """
    if int(limit) < 0:
        filters.limit = 25
    else:
        filters.limit = limit


def _validate_offset(filters: GameRequestFilters, offset: int) -> None:
    if int(offset) < 0:
        offset = None

    filters.offset = offset


def _validate_ordering_rules(
    filters: GameRequestFilters, order: str, order_by: str
) -> None:
    if _order_missing_pair(order, order_by):
        if order is None:
            raise GameValidationError(
                "order parameter cannot be null when orderBy parameter exists",
                ["order"],
            )
        elif order_by is None:
            raise GameValidationError(
                "orderBy parameter cannot be null when order parameter exists",
                ["order_by"],
            )
    elif not _order_equals_allowed_value(order):
        raise GameValidationError(
            'order value must be one of the allowed values ["ASC", "DESC"]', ["order"]
        )

    filters.order = str.upper(order)

    if not _order_by_equals_allowed_value(order_by):
        raise GameValidationError(
            "order query must be one of the allowed values ['date', 'title']",
            ["order_by"],
        )

    filters.order_by = str.lower(order_by)


def _order_equals_allowed_value(order: str) -> bool:
    """
    Order validation, if provided. Must be one of allowed values: ASC for
    acending order or DESC for decending order
    """
    return order == "ASC" or order == "DESC"


def _order_by_equals_allowed_value(order_by: str) -> bool:
    valid_values = ["title", "date"]
    regex = re.compile(BASIC_TEXT_REGEX_PATTERN)
    order_by_value_matches = regex.match(order_by)
    if order_by_value_matches is None:
        raise GameValidationError("Order by value in unrecognized format", ["order_by"])

    filtered_order_by = str.lower(order_by).strip()
    return filtered_order_by in valid_values


def _order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None)
        or (order is not None and order_by is not None)
    )


def _validate_game_id_filter(filters: GameRequestFilters, game_id: str) -> None:
    # Game ID validation, if provided. Must be Non-null str and match UUI4 format
    if type(game_id) is not str:
        raise GameValidationError(
            "Game id must be a string in UUIDv5 format", ["game_id"]
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    game_id_matches = regex.match(game_id)
    if game_id_matches is None:
        raise GameValidationError(
            "Game id must be a string in UUIDv5 format", ["game_id"]
        )

    filters.game_id = game_id


def _validate_date_filter(filters: GameRequestFilters, date: str) -> None:
    # Date filter validation. Should be in yyyy/mm/dd format
    try:
        filtered_date = datetime.strptime(date, "%Y/%m/%d")
    except ValueError:
        raise GameValidationError(
            "filter.date must be in yyyy/mm/dd format", ["filter.date"]
        )

    filters.date = filtered_date


def validate_get_games_query_parameters(
    query_params: dict,
) -> GameRequestFilters | GameValidationError:
    filters = GameRequestFilters()

    # Get all query param values, or none if none provided
    game_id = query_params.get("filter.gameId")
    date = query_params.get("filter.date")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if game_id is not None:
        _validate_game_id_filter(filters, game_id)

    if date is not None:
        _validate_date_filter(filters, date)

    if limit is not None:
        _validate_limit(filters, limit)

    if offset is not None:
        _validate_offset(filters, offset)

    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters

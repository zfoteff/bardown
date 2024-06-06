import re

from errors.games_errors import GameValidationError
from games.models.game_request_filters import GameRequestFilters


def _validate_limit(filters: GameRequestFilters, limit: int) -> None:
    """
    Limit validation, if provided. Must be a non-null, positive integer. Defaults to 25
    if no value provided
    """
    if int(limit) < 0:
        filters.limit = 10
    else:
        filters.limit = limit

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
        raise GameValidationError("Order by value in unrecognized format", ['order_by'])

    filtered_order_by = str.lower(order_by).strip()
    return str.lower(order_by) in valid_values


def _order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None)
        or (order is not None and order_by is not None)
    )


def _validate_game_id_filter(filters: GameRequestFilters, game_id: str) -> None:
    # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
    if type(game_id) is not str:
        raise GameValidationError("Game id must be a string in UUIDv5 format", ["game_id"])

    regex = re.compile(UUID_REGEX_PATTERN)
    game_id_matches = regex.match(game_id)
    if game_id_matches is None:
        raise GameValidationError("Game id must be a string in UUIDv5 format", ["game_id"])

    filters.game_id = game_id

def _validate_date_filter(filters: GameRequestFilters,)

def validate_get_games_query_parameters(
    query_params: dict,
) -> GameRequestFilters | GameValidationError:
    filters = GameRequestFilters()

    return filters

from errors.statistics_errors import StatisticsValidationError
from stats.api.validators import UUID_REGEX_PATTERN
from stats.models.statistics_request_filters import (
    GameStatisticsRequestFilters,
    SeasonStatisticsRequestFilters,
)


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


def _validate_ordering_rules(
    filters: SeasonStatisticsRequestFilters | GameStatisticsRequestFilters,
    order: str,
    order_by: str,
) -> None:
    if _order_missing_pair(order, order_by):
        if order is None:
            raise StatisticsValidationError(
                "order parameter cannot be null when orderBy parameter exists"
            )
        elif order_by is None:
            raise StatisticsValidationError(
                "orderBy parameter cannot be null when order parameter exists"
            )
    elif not _order_equals_allowed_value(order):
        raise StatisticsValidationError(
            'order value must be one of the allowed values ["ASC", "DESC"]'
        )

    filters.order = str.upper(order)

    if not _order_by_equals_allowed_value(order_by):
        raise StatisticsValidationError(
            "order query must be one of the allowed values ['first_name'. 'last_name', 'number']"
        )

    filters.order_by = str.lower(order_by)


def _validate_player_id_filter(filters: Sta, SESRequestFilters, player_id: str) -> None:
    # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
    if type(player_id) is not str:
        raise PlayerValidationError("PlayerId must be a string in UUIDv5 format")

    regex = re.compile(UUID_REGEX_PATTERN)
    player_id_matches = regex.match(player_id)
    if player_id_matches is None:
        raise PlayerValidationError("PlayerId must be a string in UUIDv5 format")

    filters.player_id = player_id


def validate_get_season_statistics_query_parameters(
    query_params: dict,
) -> SeasonStatisticsRequestFilters | StatisticsValidationError:
    pass


def validate_get_game_statistics_query_parameters(
    query_params: dict,
) -> GameStatisticsRequestFilters | StatisticsValidationError:
    pass

import re

from errors.statistics_errors import StatisticsValidationError
from src.stats.api.validators import UUID_REGEX_PATTERN
from src.stats.models.statistics_request_filters import (
    CompositeStatisticsRequestFilters,
    GameStatisticsRequestFilters,
    SeasonStatisticsRequestFilters,
)


def _validate_limit(filters, limit: int) -> None:
    if int(limit) < 0:
        # Limit validation, if provided. Must be a non-null, positive integer
        filters.limit = 25
    else:
        filters.limit = limit


def _validate_offset(filters, offset: int) -> None:
    if int(offset) < 0:
        offset = None

    filters.offset = offset


def _order_equals_allowed_value(order: str) -> bool:
    return order == "ASC" or order == "DESC"


def _order_by_equals_allowed_value(order_by: str) -> bool:
    valid_values = ["number", "first_name", "last_name", "grade", "school"]
    return str.lower(order_by) in valid_values


def _order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None) or (order is not None and order_by is not None)
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


def _validate_player_id_filter(filters, player_id: str) -> None:
    # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
    if type(player_id) is not str:
        raise StatisticsValidationError("PlayerId must be a string in UUIDv5 format")

    regex = re.compile(UUID_REGEX_PATTERN)
    player_id_matches = regex.match(player_id)
    if player_id_matches is None:
        raise StatisticsValidationError("PlayerId must be a string in UUIDv5 format")

    filters.player_id = player_id


def _validate_game_id_filter(filters, game_id: str) -> None:
    # GameID validation, if provided. Must be Non-null str and match UUI4 format
    if type(game_id) is not str:
        raise StatisticsValidationError("GameId must be a string in UUIDv5 format")

    regex = re.compile(UUID_REGEX_PATTERN)
    game_id_matches = regex.match(game_id)
    if game_id_matches is None:
        raise StatisticsValidationError("GameId must be a string in UUIDv5 format")

    filters.player_id = game_id


def _validate_team_id_filter(filters, game_id: str) -> None:
    # TeamID validation, if provided. Must be Non-null str and match UUI4 format
    if type(game_id) is not str:
        raise StatisticsValidationError("TeamId must be a string in UUIDv5 format")

    regex = re.compile(UUID_REGEX_PATTERN)
    game_id_matches = regex.match(game_id)
    if game_id_matches is None:
        raise StatisticsValidationError("TeamId must be a string in UUIDv5 format")

    filters.player_id = game_id


def _validate_year_filter(filters: SeasonStatisticsRequestFilters, year: str) -> None:
    try:
        valid_year = int(year)
    except ValueError:
        raise StatisticsValidationError("Year must be a valid integer ")

    if valid_year < 0:
        raise StatisticsValidationError("Year must not a negative integer")

    filters.year = valid_year


def validate_get_game_statistics_query_parameters(
    query_params: dict,
) -> GameStatisticsRequestFilters | StatisticsValidationError:
    filters = GameStatisticsRequestFilters()

    player_id = query_params.get("filter.playerId")
    game_id = query_params.get("filter.gameId")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if player_id is not None:
        _validate_player_id_filter(filters, player_id)
    if game_id is not None:
        _validate_game_id_filter(filters, game_id)
    if limit is not None:
        _validate_limit(filters, limit)
    if offset is not None:
        _validate_offset(filters, offset)
    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters


def validate_get_season_statistics_query_parameters(
    query_params: dict,
) -> SeasonStatisticsRequestFilters | StatisticsValidationError:
    filters = SeasonStatisticsRequestFilters()

    player_id = query_params.get("filter.playerId")
    team_id = query_params.get("filter.teamId")
    year = query_params.get("filter.year")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if player_id is not None:
        _validate_player_id_filter(filters, player_id)
    if team_id is not None:
        _validate_team_id_filter(filters, team_id)
    if year is not None:
        _validate_year_filter(filters, year)
    if limit is not None:
        _validate_limit(filters, limit)
    if offset is not None:
        _validate_offset(filters, offset)
    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters


def validate_get_composite_statistics_query_parameters(
    query_params: dict,
) -> CompositeStatisticsRequestFilters | StatisticsValidationError:
    filters = CompositeStatisticsRequestFilters()

    player_id = query_params.get("filter.player.playerId")
    game_id = query_params.get("filter.game.gameId")
    team_id = query_params.get("filter.team.teamId")
    year = query_params.get("filter.year")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if player_id is not None:
        _validate_player_id_filter(filters, player_id)
    if team_id is not None:
        _validate_team_id_filter(filters, team_id)
    if game_id is not None:
        _validate_game_id_filter(filters, game_id)
    if year is not None:
        _validate_year_filter(filters, year)
    if limit is not None:
        _validate_limit(filters, limit)
    if offset is not None:
        _validate_offset(filters, offset)
    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters

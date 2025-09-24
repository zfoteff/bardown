import re

from errors.teams_errors import TeamValidationError
from teams.models.dto.team_coach import TeamCoach
from teams.models.dto.team_player import TeamPlayer
from teams.models.team_request_filters import (
    CompositeTeamRequestFilters,
    TeamRequestFilters,
)
from validators import BASIC_TEXT_REGEX_PATTERN, NAME_REGEX_PATTERN, UUID_REGEX_PATTERN


def _validate_limit(filters: TeamRequestFilters, limit: int) -> None:
    """
    Limit validation, if provided. Must be a non-null, positive integer. Defaults to 25
    if no value provided
    """
    if int(limit) < 0:
        filters.limit = 25
    else:
        filters.limit = limit


def _validate_offset(filters: TeamRequestFilters, offset: int) -> None:
    if int(offset) < 0:
        offset = None

    filters.offset = offset


def _validate_ordering_rules(
    filters: TeamRequestFilters, order: str, order_by: str
) -> None | TeamValidationError:
    if _order_missing_pair(order, order_by):
        if order is None:
            raise TeamValidationError(
                "order parameter cannot be null when orderBy parameter exists",
                ["order"],
            )
        elif order_by is None:
            raise TeamValidationError(
                "orderBy parameter cannot be null when order parameter exists",
                ["order_by"],
            )
    elif not _order_equals_allowed_value(order):
        raise TeamValidationError(
            'order value must be one of the allowed values ["ASC", "DESC"]', ["order"]
        )

    filters.order = str.upper(order)

    if not _order_by_equals_allowed_value(order_by):
        raise TeamValidationError(
            "order query must be one of the allowed values ['name']",
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
    valid_values = ["name"]
    regex = re.compile(BASIC_TEXT_REGEX_PATTERN)
    order_by_value_matches = regex.match(order_by)
    if order_by_value_matches is None:
        raise TeamValidationError("Order by value in unrecognized format", ["order_by"])

    filtered_order_by = str.lower(order_by).strip()
    return filtered_order_by in valid_values


def _order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None) or (order is not None and order_by is not None)
    )


def _validate_team_id_filter(
    filters: TeamRequestFilters | CompositeTeamRequestFilters, team_id: str
) -> None:
    # Team ID validation, if provided. Must be Non-null str and match UUI4 format
    if type(team_id) is not str:
        raise TeamValidationError(
            "filter.teamId must be a string in UUIDv5 format", ["filter.teamId"]
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    team_id_matches = regex.match(team_id)
    if team_id_matches is None:
        raise TeamValidationError("Team ID must be a string in UUIDv5 format", ["filter.teamId"])

    filters.team_id = team_id


def _validate_player_id_filter(filters: CompositeTeamRequestFilters, player_id: str) -> None:
    # Team ID validation, if provided. Must be Non-null str and match UUI4 format
    if type(player_id) is not str:
        raise TeamValidationError(
            "filter.player.id must be a string in UUIDv5 format", ["filter.player.id"]
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    player_id_matches = regex.match(player_id)
    if player_id_matches is None:
        raise TeamValidationError(
            "Player ID must be a string in UUIDv5 format", ["filter.player.id"]
        )

    filters.player_id = player_id


def _validate_team_name_filter(filters: TeamRequestFilters, name: str) -> None:
    # Name filter validation
    regex = re.compile(NAME_REGEX_PATTERN)
    name_matches = regex.match(name)

    if name_matches is None:
        raise TeamValidationError("filter.team.name is invalid", ["filter.team.name"])

    filters.team_name = name


def _validate_team_name_filter(filters: CompositeTeamRequestFilters, team_name: str) -> None:
    regex = re.compile(NAME_REGEX_PATTERN)
    name_matches = regex.match(team_name)

    if name_matches is None:
        raise TeamValidationError("filter.team.name is invalid", ["filter.team.name"])

    filters.team_name = team_name


def _validate_year_filter(filters: CompositeTeamRequestFilters, year: str) -> None:
    try:
        valid_year = int(year)
    except ValueError:
        raise TeamValidationError("Year must be a valid integer", ["filter.year"])

    if valid_year < 0:
        raise TeamValidationError("Year must not a negative integer", ["filter.year"])

    filters.year = valid_year


def validate_get_teams_query_parameters(
    query_params: dict,
) -> TeamRequestFilters | TeamValidationError:
    filters = TeamRequestFilters()

    # Get all query param values, or none if absent
    team_id = query_params.get("filter.teamId")
    name = query_params.get("filter.name")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if team_id is not None:
        _validate_team_id_filter(filters, team_id)

    if name is not None:
        _validate_team_name_filter(filters, name)

    if limit is not None:
        _validate_limit(filters, limit)

    if offset is not None:
        _validate_offset(filters, offset)

    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters


def validate_get_composite_team_query_parameters(
    query_params: dict,
) -> CompositeTeamRequestFilters | TeamValidationError:
    filters = CompositeTeamRequestFilters()

    # Get all query param values, or none if absent
    team_id = query_params.get("filter.team.id")
    player_id = query_params.get("filter.player.id")
    team_name = query_params.get("filter.team.name")
    year = query_params.get("filters.year")

    if team_id is not None:
        _validate_team_id_filter(filters, team_id)

    if player_id is not None:
        _validate_player_id_filter(filters, player_id)

    if team_name is not None:
        _validate_team_name_filter(filters, team_name)

    if year is not None:
        _validate_year_filter(filters, year)

    return filters


def validate_team_player_request(
    team_player_request: TeamPlayer,
) -> TeamPlayer | TeamValidationError:
    # TODO: Add more validation for team player post body + other post requests
    return team_player_request


def validate_team_coach_request(team_coach_request: TeamCoach) -> TeamCoach | TeamValidationError:
    # TODO: Add more validation for team coach post body
    return team_coach_request

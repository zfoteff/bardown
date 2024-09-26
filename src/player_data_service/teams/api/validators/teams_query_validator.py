import re

from errors.teams_errors import TeamValidationError
from teams.api.validators import (
    BASIC_TEXT_REGEX_PATTERN,
    NAME_REGEX_PATTERN,
    UUID_REGEX_PATTERN,
)
from teams.models.team_request_filters import TeamRequestFilters


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
) -> None:
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
        (order is None and order_by is None)
        or (order is not None and order_by is not None)
    )


def _validate_team_id_filter(filters: TeamRequestFilters, team_id: str) -> None:
    # PlayerID validation, if provided. Must be Non-null str and match UUI4 format
    if type(team_id) is not str:
        raise TeamValidationError(
            "filter.teamId must be a string in UUIDv5 format", ["filter.teamId"]
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    team_id_matches = regex.match(team_id)
    if team_id_matches is None:
        raise TeamValidationError(
            "PlayerId must be a string in UUIDv5 format", ["filter.teamId"]
        )

    filters.team_id = team_id


def _validate_name_filter(filters: TeamRequestFilters, name: str) -> None:
    # Name filter validation
    regex = re.compile(NAME_REGEX_PATTERN)
    name_matches = regex.match(name)

    if name_matches is None:
        raise TeamValidationError("filter.name is invalid", ["filter.name"])

    filters.name = name


def validate_get_teams_query_parameters(
    query_params: dict,
) -> TeamRequestFilters | TeamValidationError:
    filters = TeamRequestFilters()

    # Get all query param values, or none if none provided
    team_id = query_params.get("filter.teamId")
    name = query_params.get("filter.name")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if team_id is not None:
        _validate_team_id_filter(filters, team_id)

    if name is not None:
        _validate_name_filter(filters, name)

    if limit is not None:
        _validate_limit(filters, limit)

    if offset is not None:
        _validate_offset(filters, offset)

    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters

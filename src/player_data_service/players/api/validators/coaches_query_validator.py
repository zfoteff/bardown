import re

from src.player_data_service.errors.coaches_errors import CoachValidationError
from src.player_data_service.player.models.dto.coaches_request_filters import (
    CoachesRequestFilters,
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


def _validate_limit(filters: CoachesRequestFilters, limit: int) -> None:
    if int(limit) < 0:
        # Limit validation, if provided. Must be a non-null, positive integer
        filters.limit = 10
    else:
        filters.limit = limit


def _validate_offset(filters: CoachesRequestFilters, offset: int) -> None:
    if int(offset) < 0:
        offset = None

    filters.offset = offset


def _validate_coach_id_filter(filters: CoachesRequestFilters, coach_id: str) -> None:
    # CoachID validation, if provided. Must be non-null str in UUID4 format
    if type(coach_id) != str:
        raise CoachValidationError(
            "CoachId must be a string in UUIDv4 format", invalid_fields=list("coach_id")
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    coach_id_matches = regex.match(coach_id)
    if coach_id_matches is None:
        raise CoachValidationError("", invalid_fields=list("coach_id"))

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

def validate_get_coaches_query_parameters(query_params: dict) -> CoachesRequestFilters | CoachValidationError:
    filters = CoachesRequestFilters()

    # Get all query param values, or none if none provided
    coach_id = query_params.get("filter.coachId")
    first_name = query_params.get("filter.firstName")
    last_name = query_params.get("filter.lastName")
    role = query_params.get("filter.role")
    limit = query_params.get("limit")
    offset = query_params.get("offset")
    order = query_params.get("order")
    order_by = query_params.get("orderBy")

    if coach_id is not None:
        _validate_coach_id_filter(filters, coach_id)

    if first_name is not None or last_name is not None:

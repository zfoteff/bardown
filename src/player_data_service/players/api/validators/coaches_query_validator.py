import re

from errors.coaches_errors import CoachValidationError
from players.api.validators import NAME_REGEX_PATTERN, UUID_REGEX_PATTERN
from players.models.coaches_request_filters import CoachesRequestFilters


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


def _validate_coach_id_filter(filters: CoachesRequestFilters, coach_id: str) -> None:
    # CoachID validation, if provided. Must be non-null str in UUID5 format
    if type(coach_id) is not str:
        raise CoachValidationError(
            "CoachId must be a string in UUIDv4 format", invalid_fields=list("coach_id")
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    coach_id_matches = regex.match(coach_id)
    if coach_id_matches is None:
        raise CoachValidationError(
            "PlayerId must be a string in UUIDv5 format",
            invalid_fields=list("coach_id"),
        )


def _validate_name_filter(
    filters: CoachesRequestFilters, first_name: str, last_name: str
) -> None:
    # Name filter validation. Both first and last name must be provided, and match regex filter
    if _name_missing_pair(first_name, last_name):
        if first_name is None:
            raise CoachValidationError(
                "filter.firstName must both be provided with filter.lastName to filter results."
            )

        if last_name is None:
            raise CoachValidationError(
                "filter.lastName must both be provided with filter.firstName to filter results."
            )

    regex = re.compile(NAME_REGEX_PATTERN)
    first_name_matches = regex.match(str.capitalize(first_name))
    last_name_matches = regex.match(str.capitalize(last_name))

    if first_name_matches is None:
        raise CoachValidationError("filter.firstName is invalid.")

    if last_name_matches is None:
        raise CoachValidationError("filter.lastName is invalid.")

    filters.first_name = first_name
    filters.last_name = last_name


def _validate_role_filter(filters: CoachesRequestFilters, role: str) -> None:
    filters.role = role


def _validate_ordering_rules(
    filters: CoachesRequestFilters, order: str, order_by: str
) -> None:
    if _order_missing_pair(order, order_by):
        if order is None:
            raise CoachValidationError(
                "order parameter cannot be null when orderBy parameter exists"
            )
        elif order_by is None:
            raise CoachValidationError(
                "orderBy parameter cannot be null when order parameter exists"
            )
    elif not _order_equals_allowed_value(order):
        raise CoachValidationError(
            'order value must be one of the allowed values ["ASC", "DESC"]'
        )

    filters.order = str.upper(order)

    if not _order_by_equals_allowed_value(order_by):
        raise CoachValidationError(
            "order query must be one of the allowed values ['first_name'. 'last_name', 'number']"
        )

    filters.order_by = str.lower(order_by)


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


def validate_get_coaches_query_parameters(
    query_params: dict,
) -> CoachesRequestFilters | CoachValidationError:
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
        _validate_name_filter(filters, first_name, last_name)

    if role is not None:
        _validate_role_filter(filters, role)

    if limit is not None:
        _validate_limit(filters, limit)

    if offset is not None:
        _validate_offset(filters, offset)

    if order is not None or order_by is not None:
        _validate_ordering_rules(filters, order, order_by)

    return filters

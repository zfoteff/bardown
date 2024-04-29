import re

from src.player_data_service.errors.coaches_errors import CoachValidationError


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


def _validate_coach_id_filter(filters: CoachRequestFilters, coach_id: str) -> None:
    # CoachID validation, if provided. Must be non-null str in UUID4 format
    if type(coach_id) != str:
        raise CoachValidationError(
            "CoachId must be a string in UUIDv4 format", invalid_fields=list("coach_id")
        )

    regex = re.compile(UUID_REGEX_PATTERN)
    coach_id_matches = regex.match(coach_id)
    if coach_id_matches is None:
        raise CoachValidationError("", invalid_fields=list("coach_id"))

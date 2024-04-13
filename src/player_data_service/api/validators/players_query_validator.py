from typing import Tuple

from src.player_data_service.errors.player_validation_error import PlayerValidationError


def validate_players(
    limit: int, offset: int, order: str, orderBy: str
) -> Tuple | PlayerValidationError:
    valid_limit = limit
    valid_offset = offset
    valid_order = (order, orderBy)

    if _order_missing_pair(order, orderBy):
        if order is None:
            raise PlayerValidationError(
                "Order parameter cannot be null when Order By parameter exists"
            )
        elif orderBy is None:
            raise PlayerValidationError(
                "Order By parameter cannot be null when Order parameter exists"
            )
    elif order is None and orderBy is None:
        valid_order = None
    elif not _order_equals_allowed_value(order):
        raise PlayerValidationError(
            'Order value must be one of the allowed values ["ASC", "DESC"]'
        )

    return valid_limit, valid_offset, valid_order


def _order_equals_allowed_value(order: str) -> bool:
    return order == "ASC" or order == "DESC"


def _order_missing_pair(order: str, orderBy: str) -> bool:
    return not (
        (order is None and orderBy is None)
        or (order is not None and orderBy is not None)
    )

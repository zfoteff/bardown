def order_equals_allowed_value(order: str) -> bool:
    """
    Order validation, if provided. Must be one of allowed values: ASC for
    acending order or DESC for decending order
    """
    return order == "ASC" or order == "DESC"


def order_missing_pair(order: str, order_by: str) -> bool:
    return not (
        (order is None and order_by is None) or (order is not None and order_by is not None)
    )


def validate_field_is_uuid(uuid: str) -> bool:
    if type(uuid) is not str:
        return False

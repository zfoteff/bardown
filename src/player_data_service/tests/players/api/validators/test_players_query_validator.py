import pytest
from bin.logger import Logger
from errors.players_errors import PlayerValidationError
from players.api.validators.players_query_validator import (
    validate_get_players_query_parameters as validate,
)
from tests.bin.decorators.timed import timed
from tests.constants import VALID_PLAYER

logger = Logger("test")


@timed(logger)
def test_validate_playerid() -> None:
    query_params = {"filter.playerId": VALID_PLAYER["player_id"]}
    filters = validate(query_params)
    assert (
        filters is not None
        and filters.player_id is not None
        and filters.player_id == VALID_PLAYER["player_id"]
    )


@timed(logger)
def test_validate_query_params_with_all_values() -> None:
    query_params = {
        "filter.playerId": VALID_PLAYER["player_id"],
        "filter.firstName": VALID_PLAYER["first_name"],
        "filter.lastName": VALID_PLAYER["last_name"],
        "limit": 10,
        "order": "ASC",
        "orderBy": "number",
    }
    filters = validate(query_params)
    assert filters is not None
    assert (
        filters.player_id is not None and filters.player_id == VALID_PLAYER["player_id"]
    )
    assert (
        filters.first_name is not None
        and filters.first_name == VALID_PLAYER["first_name"]
    )
    assert (
        filters.last_name is not None and filters.last_name == VALID_PLAYER["last_name"]
    )
    assert filters.limit is not None and filters.limit == 10
    assert filters.limit is not None and filters.order == "ASC"
    assert filters.order_by is not None and filters.order_by == "number"


@timed(logger)
def test_invalidate_incorrect_playerId() -> None:
    with pytest.raises(PlayerValidationError) as err:
        query_params = {"filter.playerId": 123}
        _ = validate(query_params)

    assert "PlayerId must be a string in UUIDv5 format" == str(err.value)

    with pytest.raises(PlayerValidationError) as err:
        query_params = {"filter.playerId": "player123"}
        _ = validate(query_params)

    assert "PlayerId must be a string in UUIDv5 format" == str(err.value)


@timed(logger)
def test_invalidate_missing_name_fields() -> None:
    with pytest.raises(PlayerValidationError) as err:
        query_params = {"filter.firstName": "name"}
        _ = validate(query_params)

    assert (
        "filter.lastName must both be provided with filter.firstName to filter results."
        == str(err.value)
    )

    with pytest.raises(PlayerValidationError) as err:
        query_params = {"filter.lastName": "name"}
        _ = validate(query_params)

    assert (
        "filter.firstName must both be provided with filter.lastName to filter results."
        == str(err.value)
    )


@timed(logger)
def test_validate_offset() -> None:
    query_params = {"offset": 50}
    filters = validate(query_params)

    assert filters.offset == 50


@timed(logger)
def test_validate_incorrect_offset() -> None:
    query_params = {"offset": -1}
    filters = validate(query_params)

    assert filters.offset is None


@timed(logger)
def test_validate_incorrect_limit() -> None:
    query_params = {"limit": -1}
    filters = validate(query_params)

    assert filters.limit == 10


@timed(logger)
def test_validate_order_rules() -> None:
    query_params = {"order": "ASC", "orderBy": "number"}
    filters = validate(query_params)

    assert filters.order == "ASC"
    assert filters.order_by == "number"


@timed(logger)
def test_invalidate_missing_order_fields() -> None:
    with pytest.raises(PlayerValidationError) as err:
        query_params = {"order": "ASC"}
        _ = validate(query_params)

    assert "orderBy parameter cannot be null when order parameter exists" == str(
        err.value
    )

    with pytest.raises(PlayerValidationError) as err:
        query_params = {"orderBy": "number"}
        _ = validate(query_params)

    assert "order parameter cannot be null when orderBy parameter exists" == str(
        err.value
    )


@timed(logger)
def test_invalidate_invalid_order_value() -> None:
    with pytest.raises(PlayerValidationError) as err:
        query_params = {"order": "up", "orderBy": "number"}
        _ = validate(query_params)

    assert 'order value must be one of the allowed values ["ASC", "DESC"]' == str(
        err.value
    )


@timed(logger)
def test_invalidate_invalid_order_by_value() -> None:
    with pytest.raises(PlayerValidationError) as err:
        query_params = {"order": "ASC", "orderBy": "experience"}
        _ = validate(query_params)

    assert (
        "order query must be one of the allowed values ['first_name'. 'last_name', 'number']"
        == str(err.value)
    )

__version__ = "1.0.0"
__author__ = "Zac Foteff"

from sys import exc_info
from fastapi import Request
import pytest
from src.logger import Logger
from src.player_data_service.errors.player_validation_error import PlayerValidationError
from src.player_data_service.players.api.validators.players_query_validator import (
    validate_get_players_query_parameters as validate,
)
from tests.bin.decorators.timed import timed
from tests.bin.constants import VALID_PLAYER

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
        filters = validate(query_params)

    assert "PlayerId must be a string in UUIDv4 format" == str(err.value)

    with pytest.raises(PlayerValidationError) as err:
        query_params = {"filter.playerId": "player123"}
        filters = validate(query_params)

    assert "PlayerId must be a string in UUIDv4 format" == str(err.value)


@timed(logger)
def test_invalidate_badly_formatted_playerId() -> None:
    pass

from models.players_filters import PlayersFilters
from tests.bin.decorators.timed import timed

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_create_empty_player_filters() -> None:
    filters = PlayersFilters()
    logger.debug(filters.to_dict())
    assert filters.to_dict() == {}


@timed(logger)
def test_create_player_filters_will_all_values() -> None:
    test_player_ids = ["id1", "id2"]
    test_first_names = ["t1", "t2"]
    test_last_names = ["t1", "t2", "t3"]
    test_positions = ["A"]
    test_numbers = ["6", "7"]
    test_grades = ["g1", "g2"]
    expected_filters = {
        "filter.playerId": str.join(",", test_player_ids),
        "filter.firstName": str.join(",", test_first_names),
        "filter.lastName": str.join(",", test_last_names),
        "filter.number": str.join(",", test_numbers),
        "filter.position": str.join(",", test_positions),
        "filter.grade": str.join(",", test_grades),
    }

    filters = PlayersFilters(
        player_ids=test_player_ids,
        first_names=test_first_names,
        last_names=test_last_names,
        numbers=test_numbers,
        positions=test_positions,
        grades=test_grades,
    )
    logger.debug(filters.to_dict())
    filter_obj = filters.to_dict()
    assert len(filter_obj.keys()) == len(expected_filters.keys())
    for key in filter_obj:
        assert key in expected_filters.keys()
        assert filter_obj[key] == expected_filters[key]


@timed(logger)
def test_create_player_filter_with_empty_values():
    filters = PlayersFilters(
        player_ids=[],
        first_names=[],
        last_names=[],
        numbers=[],
        positions=[],
        grades=[],
    )

    logger.debug(filters.to_dict())
    assert filters.to_dict() == {}


def test_create_player_filter_with_some_empty_values():
    test_player_ids = ["id1", "id2"]
    test_first_names = []
    test_last_names = []
    test_positions = []
    test_numbers = ["6", "7"]
    test_grades = ["g1", "g2"]
    expected_filters = {
        "filter.playerId": str.join(",", test_player_ids),
        "filter.number": str.join(",", test_numbers),
        "filter.grade": str.join(",", test_grades),
    }

    filters = PlayersFilters(
        player_ids=test_player_ids,
        first_names=test_first_names,
        last_names=test_last_names,
        numbers=test_numbers,
        positions=test_positions,
        grades=test_grades,
    )
    logger.debug(filters.to_dict())
    filter_obj = filters.to_dict()
    assert len(filter_obj.keys()) == len(expected_filters.keys())
    for key in filter_obj:
        assert key in expected_filters.keys()
        assert filter_obj[key] == expected_filters[key]

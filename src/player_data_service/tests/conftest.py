"""Shared pytest fixtures for player_data_service tests."""

from unittest.mock import Mock, patch

import pytest
from players.models.dto.player import Player as PlayerDTO
from players.models.players_request_filters import PlayersRequestFilters
from players.player_db_interface import PlayerDatabaseInterface


# Common test data constants
SAMPLE_PLAYER_ID = "07c48b11-acbb-4725-8f21-21468c6c7d71"
SAMPLE_PLAYER_ID_2 = "251ca100e-2563-4e4e-aa0c-c345f03d4f1a"
SAMPLE_TIMESTAMP = "2024-01-01 12:00:00"
SAMPLE_DATE = "2024-01-01"


@pytest.fixture
def sample_uuid():
    """Fixture for a sample player ID."""
    return SAMPLE_PLAYER_ID


@pytest.fixture
def sample_uuid_2():
    """Fixture for an alternate sample player ID"""
    return SAMPLE_PLAYER_ID_2


@pytest.fixture
def sample_player_dto():
    """Fixture for a sample PlayerDTO object."""
    return PlayerDTO(
        first_name="John",
        last_name="Doe",
        position="Attack",
        number=15,
        grade="Senior",
        school="Test School",
        imgurl="test.jpg",
    )


@pytest.fixture
def simple_player_dto():
    """Fixture for a simple PlayerDTO with minimal fields."""
    return PlayerDTO(first_name="John", last_name="Doe")


@pytest.fixture
def sample_player_tuple():
    """Fixture for a sample player database tuple."""
    return (
        SAMPLE_PLAYER_ID,
        "John",
        "Doe",
        "Attack",
        15,
        "Senior",
        "School1",
        "img1.jpg",
        SAMPLE_DATE,
        SAMPLE_DATE,
    )


@pytest.fixture
def sample_player_tuple_2():
    """Fixture for a second sample player database tuple."""
    return (
        SAMPLE_PLAYER_ID_2,
        "Jane",
        "Smith",
        "Defense",
        20,
        "Junior",
        "School2",
        "img2.jpg",
        "2024-01-02",
        "2024-01-02",
    )


@pytest.fixture
def mock_player_data(sample_player_tuple, sample_player_tuple_2):
    """Fixture for mock database response with multiple players."""
    return [sample_player_tuple, sample_player_tuple_2]


@pytest.fixture
def empty_filters():
    """Fixture for empty PlayersRequestFilters."""
    return PlayersRequestFilters()


@pytest.fixture
def mock_mysql_client():
    """Fixture for a mocked MySQL client."""
    mock_client = Mock()
    mock_client.execute_query.return_value = (True, None)
    return mock_client


@pytest.fixture
def mock_config():
    """Fixture for mock application config."""
    mock_config_instance = Mock()
    mock_config_instance.mysql_host = "test_host"
    mock_config_instance.mysql_user = "test_user"
    mock_config_instance.mysql_password = "test_password"
    mock_config_instance.mysql_database = "test_db"
    return mock_config_instance


@pytest.fixture
def player_db_interface(mock_config):
    """Fixture for PlayerDatabaseInterface with mocked dependencies."""
    # Create a fresh mock client for each test
    mock_client = Mock()
    mock_client.execute_query.return_value = (True, None)

    with patch("players.player_db_interface.MySQLClient", return_value=mock_client):
        with patch(
            "players.player_db_interface.application_config.get_config", return_value=mock_config
        ):
            interface = PlayerDatabaseInterface()
            # Store the mock client for test access
            interface._test_mock_client = mock_client
            yield interface

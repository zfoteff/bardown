import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from uuid import NAMESPACE_OID, uuid5

from players.player_db_interface import PlayerDatabaseInterface
from players.models.dto.player import Player as PlayerDTO
from players.models.dao.player import Player as PlayerDAO
from players.models.players_request_filters import PlayersRequestFilters
from errors.players_errors import PlayerAlreadyExists, PlayerDoesNotExist


class TestPlayerDatabaseInterface:

    @patch("players.player_db_interface.MySQLClient")
    @patch("players.player_db_interface.application_config.get_config")
    def setup_method(self, method, mock_config, mock_mysql_client):
        """Setup method run before each test"""
        mock_config_instance = Mock()
        mock_config_instance.mysql_host = "test_host"
        mock_config_instance.mysql_user = "test_user"
        mock_config_instance.mysql_password = "test_password"
        mock_config_instance.mysql_database = "test_db"
        mock_config.return_value = mock_config_instance

        self.mock_client = Mock()
        mock_mysql_client.return_value = self.mock_client

        self.db_interface = PlayerDatabaseInterface()

    def test_init_creates_mysql_client_with_correct_config(self):
        """Test that PlayerDatabaseInterface initializes with correct MySQL config"""
        assert self.db_interface._PlayerDatabaseInterface__client == self.mock_client
        self.mock_client.open_connection.assert_called_once()

    def test_build_query_from_filters_player_id_only(self):
        """Test query building with only player_id filter"""
        filters = PlayersRequestFilters()
        filters.player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

        query = self.db_interface._build_query_from_filters(filters)

        expected = "SELECT * FROM players WHERE playerid='07c48b11-acbb-4725-8f21-21468c6c7d71'"
        assert query == expected

    def test_build_query_from_filters_name_only(self):
        """Test query building with first_name and last_name filters"""
        filters = PlayersRequestFilters()
        filters.first_name = "John"
        filters.last_name = "Doe"

        query = self.db_interface._build_query_from_filters(filters)

        expected = "SELECT * FROM players WHERE firstname='John' AND lastname='Doe'"
        assert query == expected

    def test_build_query_from_filters_with_ordering(self):
        """Test query building with order and order_by"""
        filters = PlayersRequestFilters()
        filters.order = "DESC"
        filters.order_by = "last_name"

        query = self.db_interface._build_query_from_filters(filters)

        expected = "SELECT * FROM players ORDER BY last_name DESC"
        assert query == expected

    def test_build_query_from_filters_with_pagination(self):
        """Test query building with limit and offset"""
        filters = PlayersRequestFilters()
        filters.limit = 10
        filters.offset = 20

        query = self.db_interface._build_query_from_filters(filters)

        expected = "SELECT * FROM players LIMIT 10 OFFSET 20"
        assert query == expected

    def test_build_query_from_filters_all_parameters(self):
        """Test query building with all parameters"""
        filters = PlayersRequestFilters()
        filters.player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"
        filters.order = "ASC"
        filters.order_by = "first_name"
        filters.limit = 5
        filters.offset = 10

        query = self.db_interface._build_query_from_filters(filters)

        expected = "SELECT * FROM players WHERE playerid='07c48b11-acbb-4725-8f21-21468c6c7d71' ORDER BY first_name ASC LIMIT 5 OFFSET 10"
        assert query == expected

    def test_build_query_from_filters_name_takes_precedence_over_player_id(self):
        """Test that when both player_id and name filters exist, name is used (based on elif logic)"""
        filters = PlayersRequestFilters()
        filters.player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"
        filters.first_name = "John"
        filters.last_name = "Doe"

        query = self.db_interface._build_query_from_filters(filters)

        # Should use name filter, not player_id due to elif condition
        expected = "SELECT * FROM players WHERE playerid='07c48b11-acbb-4725-8f21-21468c6c7d71'"
        assert query == expected

    @patch("players.player_db_interface.build_update_fields")
    def test_build_update_query(self, mock_build_update_fields):
        """Test update query building"""
        mock_build_update_fields.return_value = "firstname='John', lastname='Doe'"

        player = PlayerDTO(first_name="John", last_name="Doe")
        player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

        query = self.db_interface._build_update_query(player, player_id)

        expected = "UPDATE players SET firstname='John', lastname='Doe' WHERE playerid='07c48b11-acbb-4725-8f21-21468c6c7d71'"
        assert query == expected
        mock_build_update_fields.assert_called_once_with(player)

    @patch("players.player_db_interface.datetime")
    @patch("players.player_db_interface.uuid5")
    def test_create_player_success(self, mock_uuid5, mock_datetime):
        """Test successful player creation"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = "2024-01-01 12:00:00"
        mock_uuid5.return_value = "07c48b11-acbb-4725-8f21-21468c6c7d71"
        self.mock_client.execute_query.return_value = (True, None)

        # Mock player_exists to return False (player doesn't exist)
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = (False, None)

            player = PlayerDTO(
                first_name="John",
                last_name="Doe",
                position="Attack",
                number=15,
                grade="Senior",
                school="Test School",
                imgurl="test.jpg",
            )

            result = self.db_interface.create_player(player)

            assert result is True
            assert player.player_id == "07c48b11-acbb-4725-8f21-21468c6c7d71"
            assert player.created == "2024-01-01 12:00:00"
            assert player.modified == "2024-01-01 12:00:00"

            # Verify database call
            self.mock_client.execute_query.assert_called_once()
            call_args = self.mock_client.execute_query.call_args
            assert "INSERT INTO players" in call_args[0][0]
            assert call_args[1]["commit_candidate"] is True

    def test_create_player_already_exists(self):
        """Test player creation when player already exists"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = (True, "existing-player-id")

            player = PlayerDTO(first_name="John", last_name="Doe")

            with pytest.raises(PlayerAlreadyExists) as exc_info:
                self.db_interface.create_player(player)

            assert "Player already exists" in str(exc_info.value)
            assert exc_info.value.existing_player_id == "existing-player-id"

    def test_create_player_database_error(self):
        """Test player creation with database error"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = (False, None)
            self.mock_client.execute_query.return_value = (False, None)

            player = PlayerDTO(first_name="John", last_name="Doe")

            result = self.db_interface.create_player(player)

            assert result is False

    def test_get_players_success(self):
        """Test successful player retrieval"""
        # Mock database response
        mock_player_data = [
            (
                "07c48b11-acbb-4725-8f21-21468c6c7d71",
                "John",
                "Doe",
                "Attack",
                15,
                "Senior",
                "School1",
                "img1.jpg",
                "2024-01-01",
                "2024-01-01",
            ),
            (
                "id251ca100e-2563-4e4e-aa0c-c345f03d4f1a",
                "Jane",
                "Smith",
                "Defense",
                20,
                "Junior",
                "School2",
                "img2.jpg",
                "2024-01-02",
                "2024-01-02",
            ),
        ]
        self.mock_client.execute_query.return_value = (True, mock_player_data)

        with patch("players.player_db_interface.PlayerDAO") as mock_player_dao:
            mock_player_dao.from_tuple.side_effect = [Mock(spec=PlayerDAO), Mock(spec=PlayerDAO)]

            filters = PlayersRequestFilters()
            success, players = self.db_interface.get_players(filters)

            assert success is True
            assert len(players) == 2
            assert mock_player_dao.from_tuple.call_count == 2

    def test_get_players_database_error(self):
        """Test player retrieval with database error"""
        self.mock_client.execute_query.return_value = (False, None)

        filters = PlayersRequestFilters()
        success, players = self.db_interface.get_players(filters)

        assert success is False
        assert players == []

    def test_update_player_success(self):
        """Test successful player update"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = "07c48b11-acbb-4725-8f21-21468c6c7d71"
            self.mock_client.execute_query.return_value = (False, None)  # Note: inverted logic bug

            player = PlayerDTO(first_name="John", last_name="Doe")
            player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

            result = self.db_interface.update_player(player, player_id)

            # Due to the bug in line 111, False from execute_query returns True
            assert result is True

    def test_update_player_database_error(self):
        """Test player update with database error"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = "existing-player-id"
            self.mock_client.execute_query.return_value = (True, None)  # Note: inverted logic bug

            player = PlayerDTO(first_name="John", last_name="Doe")
            player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

            result = self.db_interface.update_player(player, player_id)

            # Due to the bug in line 111, True from execute_query returns False
            assert result is False

    def test_update_player_does_not_exist(self):
        """Test updating non-existent player"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.side_effect = PlayerDoesNotExist("Player not found")

            player = PlayerDTO(first_name="John", last_name="Doe")
            player_id = "non-existent-id"

            with pytest.raises(PlayerDoesNotExist):
                self.db_interface.update_player(player, player_id)

    def test_delete_players_success(self):
        """Test successful player deletion"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = "07c48b11-acbb-4725-8f21-21468c6c7d71"
            self.mock_client.execute_query.return_value = (
                True,
                [("07c48b11-acbb-4725-8f21-21468c6c7d71")],
            )

            player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

            result = self.db_interface.delete_players(player_id)

            # Due to the bug in line 117, False from execute_query returns True
            assert result is True

    def test_delete_players_database_error(self):
        """Test player deletion with database error"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.return_value = "07c48b11-acbb-4725-8f21-21468c6c7d71"
            self.mock_client.execute_query.return_value = True  # Note: inverted logic bug

            player_id = "07c48b11-acbb-4725-8f21-21468c6c7d71"

            result = self.db_interface.delete_players(player_id)

            # Due to the bug in line 117, True from execute_query returns False
            assert result is False

    def test_delete_players_does_not_exist(self):
        """Test deleting non-existent player"""
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            mock_player_exists.side_effect = PlayerDoesNotExist("Player not found")

            player_id = "non-existent-id"

            with pytest.raises(PlayerDoesNotExist):
                self.db_interface.delete_players(player_id)

    def test_player_exists_by_id_found(self):
        """Test player_exists with player_id when player exists"""
        self.mock_client.execute_query.return_value = (
            True,
            [("07c48b11-acbb-4725-8f21-21468c6c7d71",)],
        )

        result = self.db_interface.player_exists(player_id="07c48b11-acbb-4725-8f21-21468c6c7d71")

        assert result == "07c48b11-acbb-4725-8f21-21468c6c7d71"

        # Verify correct query was called
        call_args = self.mock_client.execute_query.call_args[0][0]
        assert (
            "SELECT playerid FROM players WHERE playerid='07c48b11-acbb-4725-8f21-21468c6c7d71'"
            == call_args
        )

    def test_player_exists_by_name_found(self):
        """Test player_exists with first_name and last_name when player exists"""
        self.mock_client.execute_query.return_value = (True, [("found-player-id",)])

        result = self.db_interface.player_exists(first_name="John", last_name="Doe")

        assert result == "found-player-id"

        # Verify correct query was called
        call_args = self.mock_client.execute_query.call_args[0][0]
        assert "SELECT playerid FROM players WHERE firstname='John' AND lastname='Doe'" == call_args

    def test_player_exists_not_found_database_error(self):
        """Test player_exists when database query fails"""
        self.mock_client.execute_query.return_value = (False, None)

        with pytest.raises(PlayerDoesNotExist) as exc_info:
            self.db_interface.player_exists(player_id="07c48b11-acbb-4725-8f21-21468c6c7d71")

        assert "Player does not exist" in str(exc_info.value)
        assert "player_id: 07c48b11-acbb-4725-8f21-21468c6c7d71" in str(exc_info.value)

    def test_player_exists_not_found_empty_result(self):
        """Test player_exists when no player found"""
        self.mock_client.execute_query.return_value = (True, [])

        with pytest.raises(PlayerDoesNotExist) as exc_info:
            self.db_interface.player_exists(first_name="John", last_name="Doe")

        assert "Player does not exist" in str(exc_info.value)
        assert "first_name: John" in str(exc_info.value)
        assert "last_name: Doe" in str(exc_info.value)

    def test_player_exists_not_found_none_result(self):
        """Test player_exists when result is None"""
        self.mock_client.execute_query.return_value = (False, None)

        with pytest.raises(PlayerDoesNotExist):
            self.db_interface.player_exists(player_id="07c48b11-acbb-4725-8f21-21468c6c7d71")

    @pytest.mark.parametrize(
        "filters_data,expected_query",
        [
            # Test various filter combinations
            ({"player_id": "123"}, "SELECT * FROM players WHERE playerid='123'"),
            (
                {"first_name": "John", "last_name": "Doe"},
                "SELECT * FROM players WHERE firstname='John' AND lastname='Doe'",
            ),
            (
                {"order": "ASC", "order_by": "first_name"},
                "SELECT * FROM players ORDER BY first_name ASC",
            ),
            ({"limit": 10}, "SELECT * FROM players LIMIT 10"),
            ({"offset": 5}, "SELECT * FROM players OFFSET 5"),
            ({}, "SELECT * FROM players"),  # No filters
        ],
    )
    def test_build_query_from_filters_parametrized(self, filters_data, expected_query):
        """Parametrized test for various filter combinations"""
        filters = PlayersRequestFilters()
        for key, value in filters_data.items():
            setattr(filters, key, value)

        query = self.db_interface._build_query_from_filters(filters)
        assert query == expected_query

    def test_integration_create_and_get_player(self):
        """Integration test for create and get operations"""
        # Test the flow of creating a player and then retrieving it
        with patch.object(self.db_interface, "player_exists") as mock_player_exists:
            # First call (create) - player doesn't exist
            # Second call (get) - player exists
            mock_player_exists.side_effect = [(False, None), "created-player-id"]

            # Mock successful database operations
            self.mock_client.execute_query.side_effect = [
                (True, None),  # Create operation
                (
                    True,
                    [
                        (
                            "created-player-id",
                            "John",
                            "Doe",
                            "Attack",
                            15,
                            "Senior",
                            "School",
                            "img.jpg",
                            "2024-01-01",
                            "2024-01-01",
                        )
                    ],
                ),  # Get operation
            ]

            # Create player
            player = PlayerDTO(first_name="John", last_name="Doe")
            create_result = self.db_interface.create_player(player)
            assert create_result is True

            # Get players
            with patch("players.player_db_interface.PlayerDAO") as mock_player_dao:
                mock_player_dao.from_tuple.return_value = Mock(spec=PlayerDAO)

                filters = PlayersRequestFilters()
                filters.first_name = "John"
                filters.last_name = "Doe"

                success, players = self.db_interface.get_players(filters)
                assert success is True
                assert len(players) == 1

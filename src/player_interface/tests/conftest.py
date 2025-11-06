from unittest.mock import Mock, patch

import pytest

SAMPLE_PLAYER_ID = "07c48b11-acbb-4725-8f21-21468c6c7d71"
SAMPLE_PLAYER_ID_2 = "251ca100e-2563-4e4e-aa0c-c345f03d4f1a"
SAMPLE_TIMESTAMP = "2024-01-01 12:00:00"
SAMPLE_DATE = "2024-01-01"


@pytest.fixture
def sample_uuid() -> str:
    return SAMPLE_PLAYER_ID


@pytest.fixture
def sample_uuid_2() -> str:
    return SAMPLE_PLAYER_ID_2

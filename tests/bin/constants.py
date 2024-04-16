import datetime

from src.player_data_service.players.models.enums.grade import Grade
from src.player_data_service.players.models.enums.position import Position

VALID_UUID = "fb344330-0e2a-4348-9665-9061cae42aab"

VALID_PLAYER = {
    "player_id": VALID_UUID,
    "number": 6,
    "first_name": "new",
    "last_name": "player",
    "position": Position.ATTACK,
    "grade": Grade.SENIOR,
    "school": "Clackamas High School",
    "created": "2024-04-16 09:25:37",
    "modified": "2024-04-16 09:25:37",
}
VALID_PLAYER_TUPLE = (
    VALID_UUID,
    6,
    "new",
    "player",
    Position.ATTACK,
    Grade.SENIOR,
    "Clackamas High School",
    "2024-04-16 09:25:37",
    "2024-04-16 09:25:37",
)

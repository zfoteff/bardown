import datetime

from players.models.enums.grade import Grade
from players.models.enums.position import Position

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
VALID_COACH = {
    "coach_id": VALID_UUID,
    "first_name": "new",
    "last_name": "coach",
    "role": "Head Coach",
    "phone_number": "5037810087",
    "email": "email@home.com",
    "created": "2024-04-16 09:25:37",
    "modified": "2024-04-16 09:25:37",
}
VALID_COACH_TUPLE = (
    VALID_UUID,
    "new",
    "coach",
    "Head Coach",
    "5037810087",
    "email@home.com",
    "2024-04-16 09:25:37",
    "2024-04-16 09:25:37",
)

from players.models.enums.grade import Grade
from players.models.enums.position import Position

VALID_UUID_0 = "fb344330-0e2a-4348-9665-9061cae42aab"
VALID_UUID_1 = "ca10f45f-a993-4f1d-bc54-e67751dba90b"

VALID_PLAYER = {
    "player_id": VALID_UUID_0,
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
    VALID_UUID_0,
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
    "coach_id": VALID_UUID_0,
    "first_name": "new",
    "last_name": "coach",
    "role": "Head Coach",
    "phone_number": "5037810087",
    "email": "email@home.com",
    "created": "2024-04-16 09:25:37",
    "modified": "2024-04-16 09:25:37",
}
VALID_COACH_TUPLE = (
    VALID_UUID_0,
    "new",
    "coach",
    "Head Coach",
    "5037810087",
    "email@home.com",
    "2024-04-16 09:25:37",
    "2024-04-16 09:25:37",
)
VALID_GAME_STATISTICS = {
    "hsh": 4,
    "msh": 5,
    "lsh": 4,
    "hg": 2,
    "mg": 0,
    "lg": 2,
    "a": 3,
    "gb": 2,
    "t": 0,
    "ct": 1,
    "p": 1,
    "k": 0,
    "ms": 1,
    "hga": 0,
    "mga": 0,
    "lga": 0,
    "hgs": 0,
    "mgs": 0,
    "lgs": 0,
    "fow": 1,
    "fol": 2
}
VALID_GAME_STATISTICS_TUPLE = (
    VALID_UUID_0,
    VALID_UUID_1,
    "4|5|4|2|0|2|3|2|0|1|1|0|1|0|0|0|0|0|0|1|2"
)
from enum import Enum


class EventType(Enum):
    PLAYER_CREATED = "player-created"
    COACH_CREATED = "coach-created"
    TEAM_CREATED = "team-created"
    GAME_COMPLETED = "game-completed"
    GAME_CREATED = "game-created"
    PLAYER_ADDED_TO_TEAM = "player-added-to-team"
    COACH_ADDED_TO_TEAM = "coach-added-to-team"
    PLAYER_STATISTIC_UPDATE = "player-statistic-update"

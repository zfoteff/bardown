from errors.games_errors import GameValidationError
from games.models.game_request_filters import GameRequestFilters


def validate_get_games_query_parameters(
    query_params: dict,
) -> GameRequestFilters | GameValidationError:
    filters = GameRequestFilters()

    return filters

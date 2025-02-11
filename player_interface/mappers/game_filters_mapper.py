from typing import Dict, List

from models.game_filters import GameFilters


def string_to_list(data: str) -> List[str]:
    return data.replace(" ", "").split(",")


class GameFiltersMapper:
    def form_to_game_filters(form: Dict) -> GameFilters:
        filters = GameFilters()
        if "game_id" in form.keys():
            filters.team_ids = string_to_list(form["game_id"])
        if "title" in form.keys():
            filters.names = string_to_list(form["title"])
        if "date" in form.keys():
            filters.names = string_to_list(form["date"])

        return filters

from typing import Dict, List

from models.players_filters import PlayersFilters


def string_to_list(data: str) -> List[str]:
    return data.replace(" ", "").split(",")


class PlayerFiltersMapper:
    def form_to_players_filters(form: Dict) -> PlayersFilters:
        filters = PlayersFilters()
        if "player_id" in form.keys():
            filters.player_ids = string_to_list(form["player_id"])
        if "first_name" in form.keys():
            filters.first_names = string_to_list(form["first_name"])
        if "last_name" in form.keys():
            filters.last_names = string_to_list(form["last_name"])
        if "number" in form.keys():
            filters.numbers = string_to_list(form["number"])
        if "position" in form.keys():
            filters.positions = string_to_list(form["position"])
        if "grade" in form.keys():
            filters.grades = string_to_list(form["grade"])

        filters.limit = 40
        filters.order = "ASC"
        filters.order_by = "number"

        return filters
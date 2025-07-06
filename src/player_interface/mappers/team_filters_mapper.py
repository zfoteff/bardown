from typing import Dict, List

from models.team_filters import TeamFilters


def string_to_list(data: str) -> List[str]:
    return data.replace(" ", "").split(",")


class TeamFiltersMapper:
    def form_to_team_filters(form: Dict) -> TeamFilters:
        filters = TeamFilters()
        if "team_id" in form.keys():
            filters.team_ids = string_to_list(form["team_id"])
        if "name" in form.keys():
            filters.names = string_to_list(form["name"])

        return filters

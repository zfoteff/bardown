__version__ = "0.1.0"
__author__ = "Zac Foteff"

from typing import Dict, List, Self


class PlayerFilters:
    def __init__(
        self,
        player_ids: List[str] = None,
        first_names: List[str] = None,
        last_names: List[str] = None,
        numbers: List[str] = None,
        positions: List[str] = None,
        grades: List[str] = None,
    ) -> Self:
        self.player_ids = player_ids
        self.first_names = first_names
        self.last_names = last_names
        self.numbers = numbers
        self.positions = positions
        self.grades = grades

    def _should_add_contents_of_list(self, data: List) -> bool:
        return data is not None and len(data) > 0

    def to_dict(self) -> Dict:
        filters = {}

        if self._should_add_contents_of_list(self.player_ids):
            filters["filter.playerId"] = str.join(",", self.player_ids)
        if self._should_add_contents_of_list(self.first_names):
            filters["filter.firstName"] = str.join(",", self.first_names)
        if self._should_add_contents_of_list(self.last_names):
            filters["filter.lastName"] = str.join(",", self.last_names)
        if self._should_add_contents_of_list(self.positions):
            filters["filter.position"] = str.join(",", self.positions)
        if self._should_add_contents_of_list(self.numbers):
            filters["filter.number"] = str.join(",", self.numbers)
        if self._should_add_contents_of_list(self.grades):
            filters["filter.grade"] = str.join(",", self.grades)

        return filters

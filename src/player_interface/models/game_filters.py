from typing import Dict, List, Self


class GameFilters:
    def __init__(
        self,
        game_ids: List[str] = None,
        title: List[str] = None,
        date: List[str] = None,
        limit: int = 40,
        offset: int = 0,
        order: str = "ASC",
        order_by: str = "date",
    ) -> Self:
        self.game_ids = game_ids
        self.title = title
        self.date = date
        self.limit = limit
        self.offset = offset
        self.order = order
        self.order_by = order_by

    def _should_add_contents_of_list(self, data: List) -> bool:
        return data is not None and len(data) > 0

    def to_dict(self) -> Dict:
        filters = {}

        if self._should_add_contents_of_list(self.game_ids):
            filters["filter.gameId"] = str.join(",", self.game_ids)
        if self._should_add_contents_of_list(self.game_ids):
            filters["filter.title"] = str.join(",", self.title)
        if self._should_add_contents_of_list(self.date):
            filters["filter.date"] = str.join(",", self.date)

        filters["limit"] = self.limit
        filters["offset"] = self.offset
        filters["order"] = self.order
        filters["orderBy"] = self.order_by

        return filters

from typing import Self


class OrderingRules:
    def __init__(self, order: str, order_by: str) -> Self:
        self.order = order
        self.order_by = order_by

from typing import List


class PlayerValidationError(Exception):
    def __init__(self, message=None, invalid_fields: List = None):
        self.__message = message
        super().__init__(self.__message)

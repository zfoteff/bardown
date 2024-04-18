from typing import List


class CoachValidationError(Exception):
    def __init__(self, message=None, invalid_fields: List = None):
        self.__message = message
        self.invalid_fields = invalid_fields
        super().__init__(self.__message)


class CoachDoesNotExist(Exception):
    def __init__(self, message=None):
        self.__message = message
        super().__init__(self.__message)


class CoachAlreadyExists(Exception):
    def __init__(self, message=None, existing_coach_id: str = None) -> None:
        self.__message = message
        self.existing_player_id = existing_coach_id
        super().__init__(self.__message)

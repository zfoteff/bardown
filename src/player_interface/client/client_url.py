from typing import Dict, Optional, Self, List


class ClientUrl:
    def __init__(
        self,
        path: str,
        method: str,
    ) -> Self:
        self.__path: str = path
        self.__method: str = method

    @property
    def path(self) -> str:
        return self.__path

    @property
    def method(self) -> str:
        return self.__method

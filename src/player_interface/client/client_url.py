from typing import Dict, Optional, Self


class ClientUrl:
    def __init__(
        self,
        path: str,
        path_parameters: Dict[str, str] = None,
        query_parameters: dict = None,
        method: str = None,
    ) -> Self:
        self.__path: str = path
        self.__path_parameters: Optional[Dict[str, str]] = path_parameters
        self.__query_parameters: Optional[Dict[str, str]] = query_parameters
        self.__method: Optional[str] = method

    @property
    def path(self) -> str:
        return self.__path

    @property
    def path_parameters(self) -> Dict[str, str]:
        return self.__path_parameters

    @property
    def query_parameters(self) -> Dict[str, str]:
        return self.__query_parameters

    @property
    def method(self) -> str:
        return self.__method
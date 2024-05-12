from typing import Dict, Optional, Self, List


class ClientUrl:
    def __init__(
        self,
        path: str,
        method: str,
        path_parameters: List[str] = None,
        query_parameters: dict = None,
    ) -> Self:
        self.__path: str = path
        self.__method: str = method
        self.__path_parameters: Optional[Dict[str, str]] = path_parameters
        self.__query_parameters: Optional[Dict[str, str]] = query_parameters

    @property
    def path(self) -> str:
        return self.__path

    @property
    def method(self) -> str:
        return self.__method

    @property
    def path_parameters(self) -> List[str]:
        return self.__path_parameters

    @path_parameters.setter
    def path_parameters(self, new_path_parameters) -> None:
        self.__path_parameters = new_path_parameters

    @property
    def query_parameters(self) -> Dict[str, str]:
        return self.__query_parameters

    @query_parameters.setter
    def query_parameters(self, new_query_params) -> None:
        self.__query_parameters = new_query_params

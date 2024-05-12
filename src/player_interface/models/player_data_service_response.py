from typing import Self, Dict


class PlayerDataServiceResponse:
    _status: int
    _data: Dict

    def __init__(self, status: int) -> Self:
        self._status = status
        self._data

    @property
    def status(self) -> int:
        return self._status

    @property
    def data(self) -> Dict:
        return self._dict

    @data.setter
    def data(self, new_data: Dict) -> None:
        self._data = new_data

    @status.setter
    def status(self, new_status: int) -> None:
        self._status = new_status

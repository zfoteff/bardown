class EndpointConfig:
    _host: str
    _base_path: str
    _api_version: str
    _app_pathname: str
    _tls_enabled: bool = False
    _connect_timeout_ms: int
    _read_timeout_ms: int

    def __init__(
        self,
        host: str = "",
        base_path: str = "",
        api_version: str = "",
        app_pathname: str = "",
        tls_enabled: bool = False,
        connect_timeout_ms: int = 500,
        read_timeout_ms: int = 500,
    ) -> None:
        self._host = host
        self._base_path = base_path
        self._api_version = api_version
        self._app_pathname = app_pathname
        self._tls_enabled = tls_enabled
        self._connect_timeout_ms = connect_timeout_ms
        self._read_timeout_ms = read_timeout_ms

    @property
    def host(self) -> str:
        return self._host
    
    @host.setter
    def host(self, new_host: str) -> None:
        self._host = new_host

    @property
    def base_path(self) -> str:
        return self._base_path

    @base_path.setter
    def base_path(self, new_base_path: str) -> None:
        self._base_path = new_base_path

    @property
    def api_version(self) -> str:
        return self._api_version

    @api_version.setter
    def api_version(self, new_api_version: str) -> None:
        self._api_version = new_api_version

    @property
    def app_pathname(self) -> str:
        return self._app_pathname

    @app_pathname.setter
    def app_pathname(self, new_app_pathname: str) -> None:
        self._app_pathname = new_app_pathname

    @property
    def tls_enabled(self) -> bool:
        return self._tls_enabled
    
    @tls_enabled.setter
    def tls_enabled(self, new_tls_enabled: bool) -> None:
        self._tls_enabled = new_tls_enabled

    @property
    def connect_timeout_ms(self) -> int:
        return self._connect_timeout_ms

    @connect_timeout_ms.setter
    def connect_timeout_ms(self, new_connect_timeout_ms: int) -> None:
        self._connect_timeout_ms = new_connect_timeout_ms

    @property
    def read_timeout_ms(self) -> int:
        return self._read_timeout_ms

    @read_timeout_ms.setter
    def read_timeout_ms(self, new_read_timeout_ms: int) -> None:
        self._read_timeout_ms = new_read_timeout_ms

    def compose_path(self) -> str:
        """
        Create base path for all requests based on environment configuration
        """
        protocol = "https://" if self._tls_enabled else "http://"
        return (
            f"{protocol}{self.host}/{self.base_path}/{self.api_version}/{self.app_pathname}"
            if self.app_pathname is not None
            else f"{protocol}{self.host}/{self.base_path}/{self.api_version}/"
        )

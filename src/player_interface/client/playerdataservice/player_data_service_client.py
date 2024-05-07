from bin.logger import Logger
from config.player_data_service import PlayerDataServiceEndpointConfig
from models.player_data_service_response import PlayerDataServiceResponse

logger = Logger("player-data-service-client")

class PlayerDataServiceClient:
    PLAYER_COACH_ENDPOINT_PATH = "player/"
    TEAM_ENDPOINT_PATH = "team/"

    def get_players_by_filters() -> PlayerDataServiceResponse:
        pass

    def get() -> PlayerDataServiceResponse:
        pass

    def _compose_base_path(self, config: PlayerDataServiceEndpointConfig) -> str:
        return config.base_path + "/" + config.api_version + "/"
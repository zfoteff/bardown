from bin.logger import Logger
from fastapi import APIRouter
from stats.api.controller.statistics_controller import StatisticsController

API_VERSION = "v0"
STATISTICS_ROUTER = APIRouter(prefix=f"/players/{API_VERSION}")

logger = Logger("statistics-router")
# STATISTICS ROUTES
STATISTICS_ROUTER.add_api_route(
    path="/statistics/game",
    endpoint=StatisticsController.create_game_statistics,
    methods=["POST"],
    tags=["statistics"],
    responses={
        201: {
            "description": "Game statistics successfully created",
            "content": {"application/json": {"example": [{"status": 201, "data": {}}]}},
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/statistics/game",
    endpoint=StatisticsController.get_game_statistics,
    methods=["GET"],
    responses={200: {}},
)

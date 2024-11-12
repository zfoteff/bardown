from fastapi import APIRouter
from stats.api.controller.composite_statistics_controller import (
    CompositeStatisticsController,
)
from stats.api.controller.statistics_controller import StatisticsController

from bin.logger import Logger

API_VERSION = "v0"
STATISTICS_ROUTER = APIRouter(prefix=f"/statistics/{API_VERSION}")

logger = Logger("statistics-router")

# STATISTICS ROUTES
STATISTICS_ROUTER.add_api_route(
    path="/statistics/",
    endpoint=CompositeStatisticsController.get_composite_statistics,
    methods=["GET"],
    responses={200: {}},
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
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
    path="/season",
    endpoint=StatisticsController.create_season_statistics,
    methods=["POST"],
    tags=["statistics"],
    responses={
        201: {
            "description": "Season statistics successfully created",
            "content": {"application/json": {"example": [{"status": 201, "data": {}}]}},
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
    endpoint=StatisticsController.get_game_statistics,
    methods=["GET"],
    responses={200: {}},
)
STATISTICS_ROUTER.add_api_route(
    path="/season",
    endpoint=StatisticsController.get_season_statistics,
    methods=["GET"],
    responses={200: {}},
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
    endpoint=StatisticsController.delete_game_statistics,
    methods=["DELETE"],
    responses={201: {}},
)
STATISTICS_ROUTER.add_api_route(
    path="/season",
    endpoint=StatisticsController.delete_season_statistics,
    methods=["DELETE"],
    responses={201: {}},
)

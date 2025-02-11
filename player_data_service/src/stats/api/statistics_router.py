from fastapi import APIRouter

from bin.logger import Logger
from src.stats.api.controller.composite_statistics_controller import (
    CompositeStatisticsController,
)
from src.stats.api.controller.statistics_controller import StatisticsController

API_VERSION = "v0"
STATISTICS_ROUTER = APIRouter(prefix=f"/statistics/{API_VERSION}")

logger = Logger("statistics-router")

# STATISTICS ROUTES
STATISTICS_ROUTER.add_api_route(
    path="/statistics/",
    endpoint=CompositeStatisticsController.get_composite_statistics,
    methods=["GET"],
    tags=["statistics"],
    responses={
        200: {
            "description": "Composite statistics found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "data": {
                                "games": [
                                    {
                                        "game_id": "c12dc2ba-6572-46b8-95df-75da8b1b4baf",
                                        "title": "La Salle @ Aloha",
                                        "statistics": [
                                            {
                                                "player_id": "bee6c7d3-52b0-4093-af31-609c43df8f4b",
                                                "statistics": {
                                                    "hsh": 7,
                                                    "msh": 5,
                                                    "lsh": 6,
                                                    "hg": 9,
                                                    "mg": 7,
                                                    "lg": 1,
                                                    "a": 1,
                                                    "gb": 6,
                                                    "t": 4,
                                                    "ct": 6,
                                                    "p": 6,
                                                    "k": 3,
                                                    "ms": 3,
                                                    "hga": 2,
                                                    "mga": 3,
                                                    "lga": 3,
                                                    "hgs": 7,
                                                    "mgs": 5,
                                                    "lgs": 10,
                                                    "fow": 4,
                                                    "fol": 4,
                                                },
                                            }
                                        ],
                                    },
                                ],
                                "season": [
                                    {
                                        "year": 2018,
                                        "team_id": "75674569-9493-4636-827c-dd9788f93423",
                                        "team_name": "La Salle Falcons",
                                        "players": [
                                            {
                                                "player_id": "bee6c7d3-52b0-4093-af31-609c43df8f4b",
                                                "statistics": {
                                                    "hsh": 18,
                                                    "msh": 3,
                                                    "lsh": 9,
                                                    "hg": 19,
                                                    "mg": 2,
                                                    "lg": 10,
                                                    "a": 3,
                                                    "gb": 7,
                                                    "t": 10,
                                                    "ct": 9,
                                                    "p": 10,
                                                    "k": 17,
                                                    "ms": 20,
                                                    "hga": 1,
                                                    "mga": 15,
                                                    "lga": 7,
                                                    "hgs": 3,
                                                    "mgs": 5,
                                                    "lgs": 15,
                                                    "fow": 6,
                                                    "fol": 3,
                                                },
                                            }
                                        ],
                                    }
                                ],
                            }
                        }
                    ]
                }
            },
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
    endpoint=StatisticsController.create_game_statistics,
    methods=["POST"],
    tags=["statistics"],
    responses={
        201: {
            "description": "Game statistics successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": {
                                "player_id": "string",
                                "game_id": "string",
                                "statistics": {
                                    "hsh": 0,
                                    "msh": 0,
                                    "lsh": 0,
                                    "hg": 0,
                                    "mg": 0,
                                    "lg": 0,
                                    "a": 0,
                                    "gb": 0,
                                    "t": 0,
                                    "ct": 0,
                                    "p": 0,
                                    "k": 0,
                                    "ms": 0,
                                    "hga": 0,
                                    "mga": 0,
                                    "lga": 0,
                                    "hgs": 0,
                                    "mgs": 0,
                                    "lgs": 0,
                                    "fow": 0,
                                    "fol": 0,
                                },
                                "created": "2024-11-16T20:39:27.653Z",
                                "modified": "2024-11-16T20:39:27.653Z",
                            },
                        }
                    ]
                }
            },
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
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": {
                                "player_id": "string",
                                "team_id": "string",
                                "year": 0,
                                "statistics": {
                                    "hsh": 0,
                                    "msh": 0,
                                    "lsh": 0,
                                    "hg": 0,
                                    "mg": 0,
                                    "lg": 0,
                                    "a": 0,
                                    "gb": 0,
                                    "t": 0,
                                    "ct": 0,
                                    "p": 0,
                                    "k": 0,
                                    "ms": 0,
                                    "hga": 0,
                                    "mga": 0,
                                    "lga": 0,
                                    "hgs": 0,
                                    "mgs": 0,
                                    "lgs": 0,
                                    "fow": 0,
                                    "fol": 0,
                                },
                                "created": "2024-11-16T20:43:38.939Z",
                                "modified": "2024-11-16T20:43:38.939Z",
                            },
                        }
                    ]
                }
            },
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
    endpoint=StatisticsController.get_game_statistics,
    methods=["GET"],
    tags=["statistics"],
    responses={
        200: {
            "description": "Game statistics successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": [
                                {
                                    "player_id": "string",
                                    "game_id": "string",
                                    "statistics": {
                                        "hsh": 0,
                                        "msh": 0,
                                        "lsh": 0,
                                        "hg": 0,
                                        "mg": 0,
                                        "lg": 0,
                                        "a": 0,
                                        "gb": 0,
                                        "t": 0,
                                        "ct": 0,
                                        "p": 0,
                                        "k": 0,
                                        "ms": 0,
                                        "hga": 0,
                                        "mga": 0,
                                        "lga": 0,
                                        "hgs": 0,
                                        "mgs": 0,
                                        "lgs": 0,
                                        "fow": 0,
                                        "fol": 0,
                                    },
                                    "created": "2024-11-16T20:39:27.653Z",
                                    "modified": "2024-11-16T20:39:27.653Z",
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/season",
    endpoint=StatisticsController.get_season_statistics,
    methods=["GET"],
    tags=["statistics"],
    responses={
        200: {
            "description": "Season statistics successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": [
                                {
                                    "player_id": "string",
                                    "team_id": "string",
                                    "year": 0,
                                    "statistics": {
                                        "hsh": 0,
                                        "msh": 0,
                                        "lsh": 0,
                                        "hg": 0,
                                        "mg": 0,
                                        "lg": 0,
                                        "a": 0,
                                        "gb": 0,
                                        "t": 0,
                                        "ct": 0,
                                        "p": 0,
                                        "k": 0,
                                        "ms": 0,
                                        "hga": 0,
                                        "mga": 0,
                                        "lga": 0,
                                        "hgs": 0,
                                        "mgs": 0,
                                        "lgs": 0,
                                        "fow": 0,
                                        "fol": 0,
                                    },
                                    "created": "2024-11-16T20:43:38.939Z",
                                    "modified": "2024-11-16T20:43:38.939Z",
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
STATISTICS_ROUTER.add_api_route(
    path="/game",
    endpoint=StatisticsController.delete_game_statistics,
    methods=["DELETE"],
    tags=["statistics"],
    responses={204: {"description": "Game statistics successfully deleted from database"}},
)
STATISTICS_ROUTER.add_api_route(
    path="/season",
    endpoint=StatisticsController.delete_season_statistics,
    methods=["DELETE"],
    tags=["statistics"],
    responses={204: {"description": "Game statistics successfully deleted from database"}},
)

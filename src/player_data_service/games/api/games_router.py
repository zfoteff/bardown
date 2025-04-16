from fastapi import APIRouter
from games.api.controllers.game_controller import GameController

API_VERSION = "v0"
GAMES_ROUTER = APIRouter(prefix=f"/game/{API_VERSION}")

# GAME ROUTES
GAMES_ROUTER.add_api_route(
    path="/",
    endpoint=GameController.get_games,
    description="Retrieve game data from the database",
    methods=["GET"],
    tags=["games"],
    responses={
        200: {
            "description": "Games successfully found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": [
                                {
                                    "game_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "title": "Clackamas JV @ Lakeridge JV",
                                    "date": "2024-06-05 16:02:14.588405",
                                    "score": "17-12",
                                    "location": "Lakeridge High School",
                                    "included": [
                                        {
                                            "teams": {
                                                "away": {
                                                    "id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                                    "name": "Clackamas JV",
                                                },
                                                "home": {
                                                    "id": "ca10f45f-a993-4f1d-bc54-e67751dba90b",
                                                    "name": "Lakeridge JV",
                                                },
                                            },
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
GAMES_ROUTER.add_api_route(
    path="/",
    endpoint=GameController.create_game,
    description="Create game record in the database",
    methods=["POST"],
    tags=["games"],
    responses={
        201: {
            "description": "Game successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": {
                                "title": "Clackamas JV @ Lakeridge JV",
                                "date": "2024-06-05 16:02:14.588405",
                                "score": "17-12",
                                "location": "Lakeridge High School",
                            },
                        }
                    ]
                }
            },
        }
    },
)
GAMES_ROUTER.add_api_route(
    path="/",
    endpoint=GameController.update_game,
    description="Update a game record in the database",
    methods=["PATCH"],
    tags=["games"],
    responses={
        200: {
            "description": "Game successfully updated",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": {
                                "title": "Clackamas JV @ Lakeridge JV",
                                "date": "2024-06-05 16:02:14.588405",
                                "score": "17-12",
                                "location": "Lakeridge High School",
                            },
                        }
                    ]
                }
            },
        }
    },
)
GAMES_ROUTER.add_api_route(
    path="/",
    endpoint=GameController.delete_game,
    description="Delete a game record from the database",
    methods=["DELETE"],
    tags=["games"],
    responses={
        204: {
            "description": "Game successfully deleted from the database",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 204,
                            "data": {
                                "game_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                            },
                        }
                    ]
                }
            },
        }
    },
)

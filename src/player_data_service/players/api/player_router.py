from fastapi import APIRouter
from players.api.controllers.coach_controller import CoachController
from players.api.controllers.player_controller import PlayerController

API_VERSION = "v0"
PLAYER_ROUTER = APIRouter(prefix=f"/players/{API_VERSION}")

# PLAYERS ROUTES
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=PlayerController.create_player,
    description="Create player record in the database",
    methods=["POST"],
    tags=["players"],
    responses={
        201: {
            "description": "Players successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "status": 201,
                        "data": {
                            "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                            "first_name": "Zac",
                            "last_name": "Foteff",
                            "postion": "A",
                            "grade": "FR",
                            "school": "La Salle Catholic College Preparatory",
                        },
                    }
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=PlayerController.get_players,
    description="Retrieve player data from the database",
    methods=["GET"],
    tags=["players"],
    responses={
        200: {
            "description": "Players successfully found",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "data": [
                            {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                "first_name": "Zac",
                                "last_name": "Foteff",
                                "postion": "A",
                                "grade": "FR",
                                "school": "La Salle Catholic College Preparatory",
                                "created": "2024-04-16T09:25:37",
                                "modified": "2024-04-16T09:25:37",
                            }
                        ],
                    },
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=PlayerController.update_player,
    description="Update a player record in the database",
    methods=["PATCH"],
    tags=["players"],
    responses={
        200: {
            "description": "Players successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200,
                        "data": {
                            "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                            "first_name": "Zac",
                            "last_name": "Foteff",
                            "postion": "A",
                            "grade": "FR",
                            "school": "La Salle Catholic College Preparatory",
                        },
                    }
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/player",
    endpoint=PlayerController.delete_player,
    description="Delete a player record from the database",
    methods=["DELETE"],
    tags=["players"],
    responses={
        204: {
            "description": "Players successfully deleted from database",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 204,
                            "data": {
                                "player_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                            },
                        }
                    ],
                }
            },
        }
    },
)

# COACHES ROUTES
PLAYER_ROUTER.add_api_route(
    path="/coach",
    endpoint=CoachController.create_coach,
    methods=["POST"],
    tags=["coaches"],
    responses={
        201: {
            "description": "Coach successfully created",
            "content": {
                "example": {
                    "status": 201,
                    "data": {
                        "coach_id": "bfba2ab0-227c-4d80-8ec8-b80da9f0806d",
                        "first_name": "First",
                        "last_name": "Last",
                        "since": 2018,
                        "email": "email@domain.com",
                        "phone_number": "1234567890",
                        "imgurl": "static/blank.jpg",
                        "created": "2024-04-16T09:25:37",
                        "modified": "2024-04-16T09:25:37",
                    },
                }
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/coach",
    endpoint=CoachController.get_coaches,
    methods=["GET"],
    tags=["coaches"],
    responses={
        200: {
            "description": "Coaches successfully found",
            "content": {
                "example": [
                    {
                        "status": 200,
                        "data": [
                            {
                                "coach_id": "bfba2ab0-227c-4d80-8ec8-b80da9f0806d",
                                "first_name": "First",
                                "last_name": "Last",
                                "since": 2018,
                                "email": "email@domain.com",
                                "phone_number": "1234567890",
                                "imgurl": "static/blank.jpg",
                                "created": "2024-04-16T09:25:37",
                                "modified": "2024-04-16T09:25:37",
                            }
                        ],
                    }
                ]
            },
        }
    },
)
PLAYER_ROUTER.add_api_route(
    path="/coach",
    endpoint=CoachController.update_coach,
    methods=["PATCH"],
    tags=["coaches"],
    responses={
        201: {
            "description": "Coach successfully updated",
            "content": {
                "example": [
                    {
                        "status": 201,
                        "data": [
                            {
                                "coach_id": "bfba2ab0-227c-4d80-8ec8-b80da9f0806d",
                                "first_name": "First",
                                "last_name": "Last",
                                "since": 2018,
                                "email": "email@domain.com",
                                "phone_number": "1234567890",
                                "imgurl": "static/blank.jpg",
                                "created": "2024-04-16T09:25:37",
                                "modified": "2024-04-16T09:25:37",
                            }
                        ],
                    }
                ]
            },
        },
    },
)
PLAYER_ROUTER.add_api_route(
    path="/coach",
    endpoint=CoachController.delete_coach,
    methods=["DELETE"],
    tags=["coaches"],
    responses={204: {"description": "Coach successfully deleted"}},
)

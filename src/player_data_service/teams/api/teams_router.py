from fastapi import APIRouter
from teams.api.controllers.teams_controller import TeamController

API_VERSION = "v0"
TEAMS_ROUTER = APIRouter(prefix=f"/team/{API_VERSION}")

# TEAMS ROUTES
TEAMS_ROUTER.add_api_route(
    path="/",
    endpoint=TeamController.create_team,
    methods=["POST"],
    tags=["teams"],
    responses={
        201: {
            "description": "Teams successfully created",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": [
                                {
                                    "team_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "name": "La Salle Falcons",
                                    "location": "La Salle Catholic College Preparatory",
                                    "imgurl": "url",
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
TEAMS_ROUTER.add_api_route(
    path="/",
    endpoint=TeamController.get_teams,
    methods=["GET"],
    tags=["teams"],
    responses={
        200: {
            "description": "Teams successfully found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": [
                                {
                                    "team_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "name": "La Salle Falcons",
                                    "location": "La Salle Catholic College Preparatory",
                                    "imgurl": "url",
                                    "created": "2024-06-05 16:02:14.588405",
                                    "modified": "2024-06-05 16:02:14.588405",
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
TEAMS_ROUTER.add_api_route(
    path="/",
    endpoint=TeamController.update_team,
    methods=["PATCH"],
    tags=["teams"],
    responses={
        200: {
            "description": "Teams successfully updated",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": [
                                {
                                    "team_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "name": "La Salle Catholic College Preparatory Falcons",
                                    "location": "La Salle Catholic College Preparatory",
                                    "imgurl": "url",
                                    "created": "2024-06-05 16:02:14.588405",
                                    "modified": "2024-06-05 16:02:14.588405",
                                }
                            ],
                        }
                    ]
                }
            },
        }
    },
)
TEAMS_ROUTER.add_api_route(
    path="/",
    endpoint=TeamController.delete_team,
    methods=["DELETE"],
    tags=["teams"],
    responses={
        204: {
            "description": "Teams successfully deleted from the database",
        }
    },
)

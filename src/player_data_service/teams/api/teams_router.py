from fastapi import APIRouter
from teams.api.controllers.teams_coaches_controller import TeamCoachesController
from teams.api.controllers.teams_composite_controller import CompositeTeamsController
from teams.api.controllers.teams_controller import TeamController
from teams.api.controllers.teams_players_controller import TeamPlayersController

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
    path="/player",
    endpoint=TeamPlayersController.add_player_to_team_roster,
    methods=["POST"],
    tags=["teams"],
    responses={
        201: {
            "description": "Player successfully added to team roster",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": [
                                {
                                    "team_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "player_id": "a2bf04fa-bf47-46a5-90ef-c25bcc8df56c",
                                    "year": 2018,
                                    "number": 6,
                                    "position": "A",
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
    path="/player",
    endpoint=TeamPlayersController.remove_player_from_team_roster,
    methods=["DELETE"],
    tags=["teams"],
    responses={
        204: {
            "description": "Player successfully removed from team roster",
        }
    },
)
TEAMS_ROUTER.add_api_route(
    path="/coach",
    endpoint=TeamCoachesController.add_coach_to_team_roster,
    methods=["GET"],
    tags=["teams"],
    responses={
        201: {
            "description": "Coach successfully removed from team roster",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
                            "data": [
                                {
                                    "team_id": "fb344330-0e2a-4348-9665-9061cae42aab",
                                    "coach_id": "a2bf04fa-bf47-46a5-90ef-c25bcc8df56c",
                                    "year": 2018,
                                    "role": "Head Coach",
                                    "since": 2018,
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
    path="/coach",
    endpoint=TeamCoachesController.remove_coach_from_team_roster,
    methods=["DELETE"],
    tags=["teams"],
    responses={
        204: {
            "description": "Coach successfully removed from team roster",
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
        201: {
            "description": "Teams successfully updated",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 201,
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
TEAMS_ROUTER.add_api_route(
    path="/teams",
    endpoint=CompositeTeamsController.get_composite_team,
    methods=["GET"],
    tags=["teams"],
    responses={
        200: {
            "description": "Successfully retrieved composite team data for a player, coach, or a team",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": 200,
                            "data": [
                                {
                                    "team_id": "75674569-9493-4636-827c-dd9788f93423",
                                    "name": "La Salle Falcons",
                                    "location": "La Salle Catholic College Preparatory",
                                    "img_url": "static/blank.jpg",
                                    "rosters": [
                                        {
                                            "year": 2018,
                                            "players": [
                                                {
                                                    "player_id": "bee6c7d3-52b0-4093-af31-609c43df8f4b",
                                                    "first_name": "Zachary",
                                                    "last_name": "Foteff",
                                                    "position": "A",
                                                    "number": 6,
                                                    "grade": "SR",
                                                    "school": "La Salle Catholic College Preparatory",
                                                    "imgurl": "static/zac-lax.JPG",
                                                    "created": "2024-06-05 16:02:14.588405",
                                                    "modified": "2024-06-05 16:02:14.588405",
                                                }
                                            ],
                                            "coaches": [],
                                        }
                                    ],
                                },
                                {
                                    "team_id": "9873b4fa-e83d-539a-bf39-fb92519fbd25",
                                    "name": "Valhalla Club Lacrosse",
                                    "location": "Vancouver, WA",
                                    "img_url": "None",
                                    "rosters": [
                                        {
                                            "year": 2017,
                                            "players": [
                                                {
                                                    "player_id": "bee6c7d3-52b0-4093-af31-609c43df8f4b",
                                                    "first_name": "Zachary",
                                                    "last_name": "Foteff",
                                                    "position": "A",
                                                    "number": 6,
                                                    "grade": "SR",
                                                    "school": "La Salle Catholic College Preparatory",
                                                    "imgurl": "static/zac-lax.JPG",
                                                    "created": "2024-06-05 16:02:14.588405",
                                                    "modified": "2024-06-05 16:02:14.588405",
                                                }
                                            ],
                                            "coaches": [],
                                        }
                                    ],
                                },
                            ],
                        }
                    ]
                }
            },
        }
    },
)

from fastapi import APIRouter
from src.api.controllers.default_controller import DefaultController

DEFAULT_ROUTER = APIRouter()

# DEFAULT ROUTES
DEFAULT_ROUTER.add_api_route(
    "/health",
    DefaultController.get_health,
    description="Healthcheck endpoint for the Player Data Service",
    methods=["GET"],
    tags=["default"],
    responses={
        200: {
            "description": "Service is running as expected",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "status": "UP",
                            "version": "1.0.0",
                            "timestamp": 250.0,
                        }
                    ],
                }
            },
        }
    },
)

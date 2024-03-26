__version__ = "0.0.1"
__author__ = "Zac Foteff"

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from typing import List
from src.logger import Logger
from src.player_data_service.db_client import MySQLClient

logger = Logger("player-data-service-controller")


class PlayerDataServiceController:
    def __init__(self, routers: List[APIRouter]):
        self.__router = APIRouter()
        self.__db_client = MySQLClient(**config)
        self.__router.add_api_route("/health", self.get_health, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        return self.__router

    @router.get("/health")
    async def get_health(self) -> JSONResponse:
        return JSONResponse(
            status_code=200, content={"status": 200, "response": "Running"}
        )

    @router.get("/players")
    async def get_players(self) -> JSONResponse:
        players = self.__db_client.get_all_players()
        return JSONResponse (
            status_code=200, content={"status": 200: "data": players}
        )


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup events
    print("startup")
    api.include_router(player_data_service_controller.router)
    yield
    # Shutdown events
    print("shutdown")


api = FastAPI(
    title="Player Data Service",
    description="Interface for player data for the APPNAME",
    lifespan=lifespan,
    version=__version__,
)

if __name__ == "__main__":
    from uvicorn import run

    run(app="server:api", log_level="debug", reload=True)

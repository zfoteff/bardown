from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from uvicorn import run
from contextlib import asynccontextmanager

from src.logger import Logger
from src.player_data_service.db_client import MySQLClient

logger = Logger("player-data-service-controller")


class PlayerDataServiceController:
    def __init__(self):
        self.__router = APIRouter()
        self.__router.add_api_route("/health", self.get_health, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        return self.__router

    @router.get("/health")
    def get_health(self) -> JSONResponse:
        return JSONResponse(
            status_code=200, content={"status": 200, "response": "Running"}
        )
    
@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup events
    print("startup")
    yield
    # Shutdown events
    print("shutdown")

player_data_service_controller = PlayerDataServiceController()
api = FastAPI(title="Player Data Service", lifespan=lifespan)



@api.life("startup")
async def startup():
    api.include_router(player_data_service_controller.router)


if __name__ == "__main__":
    run(api)

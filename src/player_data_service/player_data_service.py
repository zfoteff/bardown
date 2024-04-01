#!/usr/bin/env python

from api.player_data_service_controller import PLAYER_DATA_SERVICE_CONTROLLER
from fastapi import FastAPI

from src.logger import Logger

logger = Logger("player-data-service")


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup events
    print("startup")
    api.include_router(PLAYER_DATA_SERVICE_CONTROLLER)
    yield
    # Shutdown events
    print("shutdown")


app = FastAPI(
    title="Player Data Service",
    description="Interface for player data for the APPNAME",
    lifespan=lifespan,
    version=__version__,
)

if __name__ == "__main__":
    from uvicorn import run

    run(app="server:app", log_level="debug", reload=True)

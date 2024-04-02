#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "v0.0.1"

from contextlib import asynccontextmanager
from logging import Logger

from api.player_data_service_controller import PLAYER_DATA_SERVICE_CONTROLLER
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from src.player_data_service.bin.metadata import servers, tags_metadata

logger = Logger("player-data-service")


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup events
    api.include_router(PLAYER_DATA_SERVICE_CONTROLLER)
    yield
    # Shutdown events


async def get_health() -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": 200, "response": "Running"})


app = FastAPI(
    title="Player Data Service",
    description="Interface for player data for the APPNAME",
    lifespan=lifespan,
    version=__version__,
    license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
    openapi_tags=tags_metadata,
    servers=servers,
)

default_router = APIRouter()
default_router.add_api_route("/health", get_health, methods=["GET"], tags=["default"])

if __name__ == "__main__":
    from uvicorn import run

    run(
        app="player_data_service:app",
        log_level="debug",
        host="0.0.0.0",
        port=3001,
        reload=True,
    )

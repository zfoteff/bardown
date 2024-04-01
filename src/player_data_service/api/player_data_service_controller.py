__version__ = "0.0.1"
__author__ = "Zac Foteff"

from contextlib import asynccontextmanager
from typing import List

from config.db_config import get_db_config
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.logger import Logger
from src.player_data_service.db_client import MySQLClient

logger = Logger("player-data-service-controller")
_db_client = MySQLClient(**get_db_config())

PLAYER_DATA_SERVICE_CONTROLLER = APIRouter()


async def get_health(self) -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": 200, "response": "Running"})


async def get_players(self) -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": 200, "data": "players"})


PLAYER_DATA_SERVICE_CONTROLLER.add_api_route("/", get_health, methods=["GET"])

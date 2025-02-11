#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "0.1.1"

import argparse
import os
import time
from contextlib import asynccontextmanager

from api.player_interface_router import PLAYER_INTERFACE_ROUTER
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from bin import metadata
from bin.logger import Logger

load_dotenv

logger = Logger("player-interface")

start_time = 0.0


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup events
    start_time = time.time()
    api.include_router(PLAYER_INTERFACE_ROUTER)
    yield
    # Shutdown events


app = FastAPI(
    title="Player Interface",
    description="Player Interface for the Bardown application",
    lifespan=lifespan,
    version=__version__,
    license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
    openapi_tags=metadata.tags,
    servers=metadata.servers,
)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    from uvicorn import run

    parser = argparse.ArgumentParser(
        description="""
        Front end for the Bardown application. Interfaces with the Player
        Data Service to display information to the user. Run with no arguments
        to start API for CRUD operations
    """
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display the version of the service",
        action="store_true",
    )
    args = parser.parse_args()

    if args.version is True:
        print(app.version)
    else:
        run(
            app="player_interface:app",
            log_level="debug",
            host="0.0.0.0",
            port=os.environ["PORT"],
            workers=1,
            reload=True,
        )

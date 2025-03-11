#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "0.1.3"

import argparse
from contextlib import asynccontextmanager

from fastapi import FastAPI
from main import PlayerDataService

from bin.metadata import servers, tags


@asynccontextmanager
async def lifespan(api: FastAPI):
    # --- Startup events ---
    # Load routes
    app = PlayerDataService()
    for route in app.routes:
        api.include_router(route)

    # Event Loop
    yield

    # Shutdown events
    app.shutdown()


app = FastAPI(
    title="Player Data Service",
    description="Interface for player data for the Bardown application",
    lifespan=lifespan,
    version=__version__,
    license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
    openapi_tags=tags,
    servers=servers,
)

if __name__ == "__main__":
    from uvicorn import run

    parser = argparse.ArgumentParser(
        description="""
        Data interface for the Bardown application. Run with no arguments to start API for CRUD operations
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
            app="player_data_service:app",
            log_level="debug",
            host="0.0.0.0",
            port="3001",
            workers=1,
            reload=True,
        )

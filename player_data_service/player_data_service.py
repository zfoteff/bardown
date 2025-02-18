#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "0.1.2"

import argparse
import os
import re
from contextlib import asynccontextmanager
from typing import Dict

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from main import PlayerDataService
from src.api.default_router import DEFAULT_ROUTER
from src.games.api.games_router import GAMES_ROUTER
from src.players.api.player_router import PLAYER_ROUTER
from src.stats.api.statistics_router import STATISTICS_ROUTER
from src.teams.api.teams_router import TEAMS_ROUTER

from bin.metadata import servers, tags

load_dotenv()


def _load_profile_configurations() -> Dict[str, str]:
    profile = os.environ["PROFILE"].strip().lower()

    if profile == "local":
        config_file = "./config/local.application.yaml"
    if profile == "local-compose":
        config_file = "./config/local-compose.application.yaml"
    if profile == "dev":
        config_file = "./config/dev.application.yaml"
    if profile == "prod":
        config_file = "./config/prod.application.yaml"

    with open(config_file) as f:
        config_content = f.read()

    def replace_env_vars(match):
        env_var_name = match.group(1)
        return os.environ.get(env_var_name, match.group(0))

    pattern = re.compile(r"\${(\w+)}")
    updated_content = re.sub(pattern, replace_env_vars, config_content)

    return yaml.safe_load(updated_content)


@asynccontextmanager
async def lifespan(api: FastAPI):
    # --- Startup events ---
    # Load profile
    config = _load_profile_configurations()

    # Load routes
    app = PlayerDataService(config=config)
    for route in app.routes:
        api.include_router(route)
        
    yield
    # Shutdown events


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
            port=os.environ["PORT"],
            workers=1,
            reload=True,
        )

#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "0.1.3"

import argparse

from player_data_service import PlayerDataService

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

    app = PlayerDataService(version=__version__)

    if args.version is True:
        print(app.version)
    else:
        run(
            app=app.app,
            log_level=app.config.get("LOG_LEVEL", "info"),
            host="0.0.0.0",
            port="3001",
            workers=1,
            reload=True,
        )

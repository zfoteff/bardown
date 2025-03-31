#!/usr/bin/env python
__author__ = "Zac Foteff"
__version__ = "0.1.3"

import argparse

from player_data_service_application import PlayerDataServiceApplication


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

    player_data_service = PlayerDataServiceApplication()

    if args.version is True:
        print(player_data_service.version)
    else:
        run(
            app=player_data_service.app,
            log_level=player_data_service.log_level,
            host="0.0.0.0",
            port="3001",
            workers=1,
            reload=True,
        )

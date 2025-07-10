#!/usr/bin/env python

import argparse

from player_interface import PlayerInterface

player_interface = PlayerInterface()

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
        print(player_interface.version)
    else:
        run(
            app=player_interface.app,
            log_level=player_interface.log_level,
            host="0.0.0.0",
            port="3000",
            workers=1,
            reload=True,
        )

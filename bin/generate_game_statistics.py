#!/usr/bin/env python

import argparse
from datetime import datetime
from typing import List

from utils import generate_statistics_string


def generate_game_statistics(game_id: str = None, player_ids: List[str] = None) -> str:
    result = ""
    for player_id in player_ids:
        result += f'("{player_id}", "{game_id}", "{generate_statistics_string(0, 10)}", "{datetime.now()}", "{datetime.now()}"),\n'
    return result[:-2] + ";"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate game statistics SQL entries")
    parser.add_argument("-g", "--game", type=str, default=None, help="Game Id")
    parser.add_argument("-p", "--players", nargs="+", default=[], help="Players Id")
    args = parser.parse_args()
    print(generate_game_statistics(args.game, args.players))


if __name__ == "__main__":
    main()

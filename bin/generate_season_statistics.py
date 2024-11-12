#!/usr/bin/env python

import argparse
from datetime import datetime
from typing import List, Tuple

from utils import generate_statistics_string


def generate_season_statistics(team_player_ids: List[Tuple[str, str]], year):
    result = ""
    for team_id, player_id in team_player_ids:
        result += f'("{player_id}", "{team_id}", {year}, "{generate_statistics_string(0, 20)}", "{datetime.now()}", "{datetime.now()}"),\n'
    return result[:-2] + ";"

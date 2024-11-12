import argparse
from datetime import datetime
from typing import List

def generate_team_players(team_id: str = None, player_ids: List[str] = None) -> str:
    result = ""
    for player_id in player_ids:
        result += f'("{player_id}", "{team_id}", "{datetime.now()}", "{datetime.now()}"),\n'
    return result[:-2] + ";"
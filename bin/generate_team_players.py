import argparse
from datetime import datetime
from typing import Dict, List


def generate_team_players(team_id: str = None, players: List[Dict] = None) -> str:
    result = ""
    time = datetime.now()
    for player in players:
        result += f'("{team_id}", "{player["id"]}", "{player["number"]}", "{player["position"]}", "{time}", "{time}"),\n'
    return result[:-2] + ";"

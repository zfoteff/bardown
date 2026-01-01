from datetime import datetime

from utils import generate_statistics_string


def generate_season_statistics(team_id: str, player_id: str, year: int):
    time = datetime.now()
    return f'("{player_id}", "{team_id}", {year}, "{generate_statistics_string(0, 20)}", "{time}", "{time}");'

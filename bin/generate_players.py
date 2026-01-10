from datetime import datetime
from random import shuffle, randint
from typing import Dict, Tuple, List
from uuid import NAMESPACE_OID, uuid5

from utils import generate_statistics_string


def generate_players(school: str, num_players: int = 11) -> Tuple[List[Dict], str]:
    positions = ["G", "D", "D", "D", "A", "A", "A", "M", "M", "M", "LSM"]
    grades = ["SR", "JR", "SO", "FR"]
    with open("first_names.txt") as f:
        first_names = [line.strip() for line in f.readlines()]
    with open("last_names.txt") as f:
        last_names = [line.strip() for line in f.readlines()]

    shuffle(first_names)
    shuffle(last_names)

    result = "INSERT INTO players VALUES "

    player_data = []
    time = datetime.now()

    for i in range(num_players):
        first_name = first_names[i]
        last_name = last_names[i]
        number = randint(0, 99)
        uuid = uuid5(namespace=NAMESPACE_OID, name=first_name + last_name)
        position = positions[i % len(positions)]
        grade = grades[randint(0, len(grades) - 1)]
        player_data.append({"id": str(uuid), "number": number, "position": position})
        result += f'("{uuid}", "{first_name}", "{last_name}", "{position}", {number}, "{grade}", "{school}", "static/blank.jpg", "{time}", "{time}"), '

    return player_data, result[:-2] + ";\n"


def generate_team_players(player_data: List[Dict], team_id: str) -> str:
    result = "INSERT INTO team_player VALUES "

    time = datetime.now()

    for player in player_data:
        result += f'("{team_id}", "{player["id"]}", 2018, {player["number"]}, "{player["position"]}", "{time}", "{time}"), '

    return result[:-2] + ";\n"

def generate_player_season_statistics(player_data: List[Dict], team_id: str) -> str:
    result = "INSERT INTO season_statistics VALUES "

    time = datetime.now()

    for player in player_data:
        result += f'("{player["id"]}", "{team_id}", 2018, "{generate_statistics_string(0, 20)}", "{time}", "{time}"), '

    return result[:-2] + ";\n"


def main():
    player_data, query = generate_players("Aloha High School")
    team_player_query = generate_team_players(player_data, "000")
    print(query)
    print(team_player_query)


if __name__ == "__main__":
    main()

from datetime import datetime
from random import shuffle, randint
from typing import Tuple, List
from uuid import NAMESPACE_OID, uuid4, uuid5


def generate_players(school: str, num_players: int = 11) -> Tuple[List[str], str]:
    positions = ["G", "D", "D", "D", "A", "A", "A", "M", "M", "M", "LSM"]
    with open("first_names.txt") as f:
        first_names = [line.strip() for line in f.readlines()]
    with open("last_names.txt") as f:
        last_names = [line.strip() for line in f.readlines()]

    shuffle(first_names)
    shuffle(last_names)

    result = "--PLAYERS\nINSERT INTO players\nVALUES\n"

    player_data = []

    for i in range(num_players):
        first_name = first_names[i]
        last_name = last_names[i]
        number = randint(0, 99)
        uuid = uuid5(namespace=NAMESPACE_OID, name=first_name + last_name)
        position = positions[i % len(positions)]
        player_data.append({"id": str(uuid), "number": number, "position": position})
        time = datetime.now()
        result += f'("{uuid}", "{first_name}", "{last_name}", "{position}", {number}, "{school}", "static/blank.jpg", "{time}", "{time}"),\n'

    return player_data, result[:-2] + ";\n"

def main():
    player_data, query = generate_players("Aloha High School")
    print(query)
    print(player_data)

if __name__ == "__main__":
    main()
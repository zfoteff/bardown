from datetime import datetime
from random import shuffle
from typing import Dict, List, Tuple
from uuid import NAMESPACE_OID, uuid5


def generate_coaches(num_coaches: int = 3) -> Tuple[List[Dict], str]:
    with open("first_names.txt") as f:
        first_names = [line.strip() for line in f.readlines()]
    with open("last_names.txt") as f:
        last_names = [line.strip() for line in f.readlines()]

    shuffle(first_names)
    shuffle(last_names)

    result = "--COACHES\nINSERT INTO coaches\nVALUES\n"

    coach_data = []
    time = datetime.now()

    for i in range(num_coaches):
        first_name = first_names[i]
        last_name = last_names[i]
        year = 2018
        uuid = uuid5(namespace=NAMESPACE_OID, name=first_name + last_name)
        phone_number = "0000000000"
        email = "email@domain"
        coach_data.append({"id": str(uuid), "year": year})
        result += f'("{uuid}", "{first_name}", "{last_name}", {year}, "{email}", "{phone_number}", "static/blank.jpg", "{time}", "{time}"),\n'

    return coach_data, result[:-2] + ";\n"


def generate_team_coaches(coach_data: List[Dict], team_id: str) -> str:
    roles = ["Head Coach", "Assistant Coach"]
    result = "--TEAM COACHES\nINSERT INTO team_coach\nVALUES\n"

    roles_counter = 0
    time = datetime.now()

    for coach in coach_data:
        role = roles[roles_counter]
        result += f'("{team_id}", "{coach["id"]}", {coach["year"]}, "{role}", {coach["year"]}, "{time}", "{time}"),\n'

        if roles_counter < len(roles) - 1:
            roles_counter += 1

    return result[:-2] + ";\n"


def main():
    coach_data, query = generate_coaches()
    team_coach = generate_team_coaches(coach_data, "000")
    print(query)
    print(team_coach)


if __name__ == "__main__":
    main()

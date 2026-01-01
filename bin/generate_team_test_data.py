from typing import Dict
from generate_coaches import generate_coaches, generate_team_coaches
from generate_players import generate_players, generate_team_players, generate_player_season_statistics
from generate_teams import generate_teams

TEAMS = [
    {
        "school_name": "Aloha High School",
        "team_name": "Aloha Warriors",
        "team_id": "a0204047-49c2-464f-b07a-261e136d10d3",
    },
    {
        "school_name": "Mt View High School",
        "team_name": "Mt. View Cougars",
        "team_id": "ea875dce-18e5-41a1-b0b1-f3eb4a6b1b9c",
    },
    {
        "school_name": "Ridgeview High School",
        "team_name": "Ridgeview Ravens",
        "team_id": "83eef374-d923-485e-8efb-6f3d226632d4",
    },
    {
        "school_name": "Liberty High School",
        "team_name": "Liberty Falcons",
        "team_id": "32f022c7-cd97-48ce-bdfc-1c336c2f0d23",
    },
    {
        "school_name": "Hood River High School",
        "team_name": "Hood River Eagles",
        "team_id": "38a1e9af-1077-4aa9-b58e-0e0f0c85afb1",
    },
    {
        "school_name": "Hillsboro High School",
        "team_name": "Hillsboro Spartans",
        "team_id": "a30e6fd4-25ba-4e89-9033-a52c42a0d296",
    },
    {
        "school_name": "West Albany High School",
        "team_name": "West Albany Bulldogs",
        "team_id": "c828a587-7a92-4cb8-b153-2014b988cdad",
    },
    {
        "school_name": "Century High School",
        "team_name": "Century Jaguars",
        "team_id": "1d4dde6f-92e0-4aac-8099-89a43fd3955b",
    },
    {
        "school_name": "Cleveland High School",
        "team_name": "Cleveland Warriors",
        "team_id": "7dcda300-b61d-4378-8f5f-e855eddd274f",
    },
    {
        "school_name": "Wilsonville High School",
        "team_name": "Wilsonville Wildcats",
        "team_id": "9bef7326-dff0-4b20-9221-b2a0d954142a",
    },
    {
        "school_name": "Tualatin High School",
        "team_name": "Tualatin Timberwolves",
        "team_id": "fc3b437d-f0ab-4177-a8cb-0ac3fe710f40",
    },
    {
        "school_name": "Sherwood High School",
        "team_name": "Sherwood Bowman",
        "team_id": "33f383a7-cb7f-4cb3-ba06-657c71f549ed",
    },
    {
        "school_name": "Tigard High School",
        "team_name": "Tigard Tigers",
        "team_id": "a2f5e394-017a-4741-b604-a7e7d3623771",
    },
    {
        "school_name": "Newberg High School",
        "team_name": "Newberg Tigers",
        "team_id": "0ddb0545-541f-40d2-962e-f222aa3d4383",
    },
    {
        "school_name": "Westview High School",
        "team_name": "Westview Tigers",
        "team_id": "9b972a51-ac44-4b63-a014-dadcf6da84c5",
    },
]
BLANK_IMG = "static/blank.jpg"


def generate_team_test_data(team: Dict) -> str:
    print(f"--- Creating {team["school_name"]} Test Data ---")
    team_result = generate_teams(team["team_id"], team["team_name"], team["school_name"])
    players, player_result = generate_players(team["school_name"])
    coaches, coach_result = generate_coaches()
    team_player_result = generate_team_players(players, team["team_id"])
    team_coach_result = generate_team_coaches(coaches, team["team_id"])
    player_season_statistics_result = generate_player_season_statistics(players, team["team_id"])

    with open(f"{team["school_name"]}-test-data.sql", "w+") as f:
        f.write(f"-- {team["school_name"]} TEST DATA --\n\n{team_result} {player_result} {team_player_result} {player_season_statistics_result} {coach_result} {team_coach_result}")

def main():
    for team in TEAMS:
        generate_team_test_data(team)


if __name__ == "__main__":
    main()

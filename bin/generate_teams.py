from datetime import datetime


def generate_teams(team_id: str, team_name: str, school_name: str):
    time = datetime.now()
    return f'-- TEAM\nINSERT INTO teams\nVALUES\n("{team_id}", "{team_name}", "{school_name}", "static/blank.jpg", "{time}", "{time}");\n'
<h1 class="service-title" style="text-align: center;">
Player Data Service
</h1>
===

![Python3](https://img.shields.io/badge/Python3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?&logo=mysql&logoColor=white)

----

Source of truth for all player, game, team, coach, and statistic data

- Future: Refactor Statistics data to its own data service

## Usage

### Local Development
Create a virtual environment for the service using pyvenv. The service requires **Python3.11** to run.

Create and run the virtual environment with all of its dependencies in the `src/player_data_service` directory with this command

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

Create a `.env` file in the `src/player_data_service` directory. Copy the keys from the `.env.dist` file to the new `.env` file and fill in the values with the application secrets. This should consist of your database connection and other configuration.

To run the application, install all dependencies with pip and run the app with the following command from the `src/player_data_service` directory

```bash
uvicorn player_data_service:app --host <HOST_IP> --port <HOST_PORT>
```

## Tips
* Ensure the application is connected to a MySQL instance with the correct schema applied

## Building
Build the application with the provided Dockerfile 

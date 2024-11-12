<h1 class="service-title" style="text-align: center;">
Player Interface
</h1>
===

![Python3](https://img.shields.io/badge/Python3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?logo=redis)

----
Interface for the Player Data Service to query for players/teams/coaches and statistics data

## Usage

### Local Development
Create a virtual environment for the service using pyvenv. The service requires **Python3.11** to run.

Create and run the virtual environment with all of its dependencies in the `src/player_interface` directory with this command

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

Create a `.env` file in the `src/player_interface` directory. Copy the keys from the `.env.dist` file to the new `.env` file and fill in the values with the application secrets. This should consist of your database connection and other configuration.

To run the application, install all dependencies with pip and run the app with the following command from the `src/player_interface` directory

```bash
uvicorn player_interface:app --host <HOST_IP> --port <HOST_PORT>
```

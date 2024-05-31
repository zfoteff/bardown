#<center><i>BARDOWN</i></center>
![](https://img.shields.io/github/commit-activity/t/zfoteff/clackamas-lacrosse-application)
![Python3](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## Overview
Player management and statistic tracking application designed for the Clackamas Lacrosse program. The application is intended to enable coaches and players to view player profiles, game and season statistics, and team affiliations.

## Contents

### Player Interface (Name W.I.P.)
Interface for the Player Data Service to query for players/teams/coaches and statistics data

![More info here.](./src/player_interface/README.md)

### Player Data Service
Source of truth for all player, team, coach, and statistic data

![More info here.](./src/player_data_service/README.md)

### Future State
- Bardown Events Listener: PubSub API for website triggered events
- Include dependency on RMQ instance
- Statistics Data Service

## Dependencies
- MySQL
- Redis Cache Instance (![Valkey](https://github.com/valkey-io/valkey) for this implementation)
- RabbitMQ

## Building and running application
A Docker Compose file is provided that will pull and build all images required to run the entire application. To run the app parts-included, run the following commands:

```bash
docker compose up # To start

docker compose down # To stop
```

Instructions to run each app individually are included in their respective README files.
BARDOWN
===

![](https://img.shields.io/github/commit-activity/t/zfoteff/clackamas-lacrosse-application)
![](https://img.shields.io/github/commits-difference/zfoteff/clackamas-lacrosse-application?base=main&head=develop&color=red)  
![Python3](https://img.shields.io/badge/Python3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?logo=rabbitmq&logoColor=white)

---

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
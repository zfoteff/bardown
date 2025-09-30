# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

BARDOWN is a player management and statistic tracking application for the Clackamas Lacrosse program, built with Python 3.11, FastAPI, MySQL, Redis/Valkey, and Docker.

## Architecture

The application follows a microservices architecture with three main components:

### Player Data Service (`src/player_data_service/`)
- Source of truth for all player, team, coach, and statistic data
- FastAPI-based REST API with MySQL database
- Entry point: `main.py`
- Main application class: `PlayerDataServiceApplication` in `player_data_service_application.py`
- Organized into domain modules: `players/`, `teams/`, `games/`, `stats/`, `api/`, `connectors/`, `validators/`

### Player Interface (`src/player_interface/`)
- Frontend web interface that queries the Player Data Service
- FastAPI application with Jinja2 templating and Redis caching
- Entry point: `main.py`
- Main application class: `PlayerInterface` in `player_interface.py`
- Serves HTML pages rendered with data from Player Data Service

### Bardown Events Listener (`src/bardown_events_listener/`)
- PubSub API for website-triggered events (currently minimal implementation)

### Bardown Lib (`src/bardown_lib/`)
- Shared library/utilities package used across services

## Development Commands

### Running the Full Application
```bash
# Start all services with Docker Compose
docker compose up

# Stop all services
docker compose down
```

### Individual Service Development

#### Player Data Service
```bash
cd src/player_data_service
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
uvicorn main:app --host <HOST_IP> --port <HOST_PORT>
```

#### Player Interface
```bash
cd src/player_interface
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
uvicorn main:app --host <HOST_IP> --port <HOST_PORT>
```

### Testing
```bash
# Run tests for specific services
cd src/player_data_service
python3 -m pytest tests/

cd src/player_interface
python3 -m pytest tests/
```

### Code Quality
```bash
# Linting and formatting (configured at root level)
flake8  # Uses .flake8 config: max-line-length=100, exclude .venv
black --line-length 100  # From pyproject.toml
isort --profile black  # From pyproject.toml
```

## Dependencies

- **Database**: MySQL (containerized as `bardown-database`)
- **Cache**: Valkey/Redis (containerized as `bardown-cache`)
- **Message Queue**: RabbitMQ (currently commented out in docker-compose.yml)

## Environment Configuration

Each service requires a `.env` file in its directory. Copy from `.env.dist` files where available and configure with appropriate database connection strings and service URLs.

## CI/CD

The project uses GitHub Actions with reusable workflows:
- `ci_python.yaml`: Python testing and Docker image building
- Service-specific workflows for `player_data_service`, `player_interface`, and `bardown_events_listener`

## Key File Patterns

- Each service has its own `pyproject.toml`, `requirements.txt`, and `dockerfile`
- Python 3.11+ is required across all services
- FastAPI is the primary web framework
- Tests are located in `tests/` directories within each service
- Main application entry points are `main.py` for both services
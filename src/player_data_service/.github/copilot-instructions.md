# Copilot Coding Agent Instructions for Player Data Service

## Overview
This service is the source of truth for player, game, team, coach, and statistic data for the "Bardown" application. It is built with FastAPI (Python 6.11) and integrates with a MySQL backend. The codebase is modular, with clear separation between API routers, controllers, database interfaces, and configuration.

## Architecture & Key Patterns
- **Entry Point**: `main.py` uses `uvicorn.run()` to launch the FastAPI app from `PlayerDataServiceApplication`.
- **App Construction**: `player_data_service_application.py` builds the FastAPI app, including routers for games, players, teams, stats, and default endpoints. Routers are registered via `include_router`, not via the `routes` parameter.
- **Routers & Controllers**: Each domain (games, players, teams, stats) has its own API router (e.g., `games/api/games_router.py`) and controller (e.g., `games/api/controllers/game_controller.py`). Endpoints are added using `add_api_route`.
- **Config & Secrets**: Configuration is managed in `config/player_data_service_config.py`. Secrets and DB connection info are loaded from `.env` (see `.env.dist` for template).
- **Database Access**: DB interfaces are in `games/games_db_interface.py`, `players/player_db_interface.py`, etc. MySQL connection logic is in `connectors/mysql.py`.
- **Error Handling**: Custom error classes are defined in `errors/` for each domain (e.g., `players_errors.py`).
- **Metadata**: OpenAPI tags and server info are set in `bin/metadata.py`.

## Developer Workflows
- **Local Development**:
  - Create and activate a Python 3.11 virtual environment in `src/player_data_service`.
  - Install dependencies: `pip install --upgrade -r requirements.txt`
  - Copy `.env.dist` to `.env` and fill in secrets.
  - Run: `uvicorn player_data_service:app --host 0.0.0.0 --port 3001`
- **Docker**:
  - Build and run using the provided `dockerfile` in the service root.
- **Debugging**:
  - Logs are written to the `logs/` directory, with separate files for each controller/router.
- **Testing**:
  - (If present) Tests are likely in domain subfolders or a dedicated `tests/` directory. Use pytest conventions.

## Project-Specific Conventions
- **API Versioning**: Routers use a versioned prefix (e.g., `/game/v0`).
- **Endpoint Registration**: Use `add_api_route` for explicit endpoint definitions, including response examples.
- **Lifespan Events**: App startup/shutdown logic is handled via an `@asynccontextmanager` static method in `player_data_service_application.py`.
- **Logging**: Use `bin/logger.py` for custom logging; logs are per-domain.
- **Error Classes**: Raise domain-specific errors from `errors/` for consistent error responses.

## Integration Points
- **MySQL**: Ensure DB schema matches expected models. Connection config is in `.env` and `config/player_data_service_config.py`.
- **External Services**: (If any) Integrate via dedicated connectors in `connectors/`.

## Examples
- Registering a new API endpoint:
  ```python
  GAMES_ROUTER.add_api_route(
      path="/",
      endpoint=GameController.get_games,
      methods=["GET"],
      tags=["games"],
      responses={...}
  )
  ```
- Adding a new router:
  ```python
  self._app.include_router(NEW_ROUTER)
  ```

## Key Files & Directories
- `main.py` — Entrypoint
- `player_data_service_application.py` — App construction
- `api/` — Routers
- `games/api/controllers/` — Controllers
- `config/` — Configuration
- `connectors/` — DB connectors
- `errors/` — Custom error classes
- `logs/` — Log files

---
If any conventions or workflows are unclear, please request clarification or examples from the user before proceeding with major changes.

# Copilot Instructions for Player Interface Codebase

## Overview & Architecture

- **Purpose**: This is a FastAPI-based frontend for the "Bardown" application, interfacing with a backend Player Data Service (PDS) and Redis cache.
- **Major Components**:
  - `main.py`: Entrypoint, starts FastAPI app via Uvicorn.
  - [`player_interface.py`](player_interface.py): Defines the FastAPI app, configures routers, static files, and app lifecycle.
  - [`api/`](api/): Contains routers, controllers, and Jinja2 HTML templates for rendering pages.
  - [`providers/`](providers/): Service layer for data access, e.g., [`player_data_service_provider.py`](providers/player_data_service_provider.py) orchestrates calls to PDS and cache.
  - [`client/`](client/): HTTP and cache clients for external service communication.
  - [`models/`](models/): Domain models, filters, requests, responses, enums.
  - [`config/`](config/): Configuration objects for endpoints, cache, and app settings.
  - [`bin/logger.py`](bin/logger.py): Custom logging utility, logs to `/logs/`.

## Developer Workflows

- **Build/Run**:
  - Local: `uvicorn player_interface:app --host <HOST_IP> --port <HOST_PORT>`
  - Docker: See [`dockerfile`](dockerfile) for containerization.
  - Debug: Use VSCode launch config in [`.vscode/launch.json`](.vscode/launch.json).
- **Testing**:
  - Tests are in [`tests/`](tests/), use `pytest` (see [`requirements.txt`](requirements.txt)).
  - Decorators like `@timed(logger)` in [`tests/bin/decorators/timed.py`](tests/bin/decorators/timed.py) are used for timing test execution.
- **Configuration**:
  - Environment variables are loaded from [`.env`](.env) (see [`config/player_interface_config.py`](config/player_interface_config.py)).
  - Endpoint and cache configs are in [`config/`](config/), e.g., [`endpoint_config.py`](config/endpoint_config.py), [`cache_config.py`](config/cache_config.py).

## Patterns & Conventions

- **Routing**: All API routes are registered in [`api/player_interface_router.py`](api/player_interface_router.py) using FastAPI's `APIRouter`.
- **Templates**: HTML pages use Jinja2 templates in [`api/templates/`](api/templates/), extending `index.html`.
- **Models**: Domain models use explicit private attributes and property getters/setters. Filters are constructed via list attributes and `.to_dict()` methods.
- **Service Layer**: Providers (e.g., [`PlayerDataServiceProvider`](providers/player_data_service_provider.py)) abstract data access, handle cache logic, and orchestrate external requests.
- **External Communication**:
  - PDS: HTTP requests via [`client/playerdataservice/player_data_service_client.py`](client/playerdataservice/player_data_service_client.py).
  - Cache: Redis via [`client/cache/cache_client.py`](client/cache/cache_client.py).
- **Custom Logging**: Use [`Logger`](bin/logger.py) for all logging; logs are written to `/logs/<key>.log`.

## Integration Points

- **Player Data Service**: Configured via [`PlayerDataServiceEndpointConfig`](config/player_data_service_endpoint_config.py), communicates over HTTP.
- **Redis Cache**: Configured via [`CacheConfig`](config/cache_config.py), used for caching API responses.
- **Static Files**: Served from `/static` (see `player_interface.py`).

## Project-Specific Details

- **Filter Mapping**: Mappers in [`mappers/`](mappers/) convert form data to filter objects (e.g., [`player_filters_mapper.py`](mappers/player_filters_mapper.py)).
- **Query Construction**: Requests use `.to_dict()` and `.query_string()` for building query parameters.
- **Error Handling**: Custom error responses for connection issues in clients/providers.
- **Versioning**: App version is set in [`player_interface.py`](player_interface.py) and surfaced via CLI and health endpoints.

## Examples

- To add a new API route, update [`api/player_interface_router.py`](api/player_interface_router.py) and implement the endpoint in [`api/controllers/player_controller.py`](api/controllers/player_controller.py).
- To add a new filter, create a model in [`models/`](models/) and a corresponding mapper in [`mappers/`](mappers/).

---

**Feedback Requested:**  
Please review for missing or unclear sections (e.g., build/test nuances, error handling, integration details). Suggest improvements or ask for clarification to iterate
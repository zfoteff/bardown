# Copilot Instructions for Clackamas Lacrosse Application

## Architecture Overview

- **Multi-service Docker Compose**: The project is organized as several services managed via `docker-compose.yml`. Key services:
  - `db`: MySQL database, initialized with `init.sql`.
  - `cache`: Redis-compatible cache (Valkey).
  - `player-data-service`: FastAPI backend for player/team/coach/statistics data.
  - `player-interface`: Frontend service that queries `player-data-service` and uses the cache.
  - (Optional) `bardown_events_listener` and `mq` (RabbitMQ) for event-driven features.

- **Data Flow**:
  - `player-interface` queries `player-data-service` for data, and uses `cache` for performance.
  - All services communicate via Docker service names (e.g., `db`, `cache`, `player-data-service`).

## Developer Workflows

- **Build & Run**:  
  Use Docker Compose for orchestration:
  ```bash
  docker compose up        # Start all services
  docker compose down      # Stop all services
  docker compose up --build # Rebuild images if Dockerfile or dependencies change
  docker compose down -v   # Remove containers and volumes (reset DB)
  ```

- **Environment Variables**:  
  Sensitive credentials (MySQL user/password) are passed via environment variables, typically set in a `.env` file at the project root.

- **Service Health**:  
  `depends_on` with healthchecks ensures services start in the correct order (e.g., `player-data-service` waits for a healthy `db`).

## Project-Specific Patterns

- **Service Discovery**:  
  Always use Docker service names (not `localhost`) for inter-service communication.  
  Example:  
  - `CACHE_HOST=cache` for connecting to the cache from `player-interface`.
  - `MYSQL_HOST=db` for connecting to MySQL from `player-data-service`.

- **Configuration**:  
  Each service reads its configuration from environment variables.  
  Example:  
  - `player-interface` expects `CACHE_HOST`, `CACHE_PORT`, etc.
  - `player-data-service` expects `MYSQL_HOST`, `MYSQL_USER`, etc.

- **Initialization**:  
  The MySQL database is initialized with `/init.sql` on first run.

## Key Files & Directories

- `docker-compose.yml`: Defines all services, volumes, and environment variables.
- `src/player_data_service/`: FastAPI backend source.
- `src/player_interface/`: Frontend source.
- `init.sql`: MySQL schema/data initialization.
- `README.md`: High-level documentation and quickstart.

## Integration Points

- **External Dependencies**:
  - MySQL (official image)
  - Valkey (Redis-compatible cache)
  - RabbitMQ (optional, commented out)
- **Internal Communication**:
  - All services communicate via Docker network using service names.

## Examples

- To connect to cache from `player-interface`, use:
  ```python
  os.getenv("CACHE_HOST", "cache")
  ```
- To reset the database, run:
  ```bash
  docker compose down -v && docker compose up --build
  ```

---

**Feedback Requested:**  
If any section is unclear or missing details (e.g., test workflow, event listener usage), please specify so instructions
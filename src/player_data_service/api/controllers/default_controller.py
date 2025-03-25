import time

from fastapi.responses import JSONResponse
from main import __version__ as player_data_service_version

start_time = time.time()


class DefaultController:
    async def get_health() -> JSONResponse:
        """Healthcheck for the Player data service. Asserts the service is running and has
        connection to database

        Returns:
            JSONResponse: Healthcheck response
        """
        return JSONResponse(
            status_code=200,
            content={
                "status": "UP",
                "version": player_data_service_version,
                "uptime": time.time() - start_time,
            },
        )

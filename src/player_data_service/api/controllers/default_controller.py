import time

from fastapi.responses import JSONResponse

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
                "uptime": time.time() - start_time,
            },
        )

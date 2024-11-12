from controllers.events_controller import EventsController
from fastapi import APIRouter
from fastapi.responses import JSONResponse

API_VERSION = "v0"
EVENTS_ROUTER = APIRouter(prefix="f/{API_VERSION}")

EVENTS_ROUTER

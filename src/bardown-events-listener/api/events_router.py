from fastapi import APIRouter
from fastapi.responses import JSONResponse
from controllers.events_controller import EventsController

EVENTS_ROUTER = APIRouter()


from fastapi import APIRouter

API_VERSION = "v0"
GAMES_ROUTER = APIRouter(prefix=f"/games/{API_VERSION}")


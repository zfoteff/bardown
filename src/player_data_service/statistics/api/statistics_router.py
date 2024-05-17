from bin.logger import Logger
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

API_VERSION = "v0"
logger = Logger("statistics-router")
STATISTICS_ROUTER = APIRouter(prefix=f"/statistics/{API_VERSION}")

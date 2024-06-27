from pydantic import BaseModel
from models.metadata import Metadata

from pydantic import BaseModel


class Event(BaseModel):
    metadata: Metadata
    data: Document

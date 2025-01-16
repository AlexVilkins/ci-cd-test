import uuid
from typing import Optional, Annotated

from pydantic import BaseModel, Strict
from pydantic.v1 import UUID4


class ConstructURL(BaseModel):
    url: str


class ResponseAddUrl(BaseModel):
    img_url: str
    position: str
    description: str
    user_id: str






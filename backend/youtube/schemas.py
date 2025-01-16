import uuid
from typing import Optional

from pydantic import BaseModel


class ConstructURL(BaseModel):
    url: str


class ResponseAllUsers(BaseModel):
    user_id: uuid.UUID
    name: str
    age: int
    city: Optional[str] = None





